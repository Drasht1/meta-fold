import pandas as pd
import requests
from pubchempy import get_compounds, get_synonyms, Compound
from tqdm import tqdm
import time
import warnings
import re
from difflib import get_close_matches
from typing import Callable, Optional

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
PUBCHEM_DELAY = 0.2  # seconds between PubChem requests
MAX_SYNONYMS_TO_TRY = 5  # limit number of synonyms to try

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

def normalize(s):
    """Normalize string by removing non-alphanumeric characters and lowercasing."""
    return re.sub(r'[^a-z0-9]', '', s.lower())

# === Cleaning Function ===
def clean_name(name):
    if pd.isnull(name):
        return ''
    name = str(name)
    name = name.split(';')[0]
    name = re.sub(r'\[[A-Za-z]+[^\]]*\]', '', name)
    name = name.replace('_', ',')
    name = re.sub(r'(?<!\s)(acid)\b', r' \1', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[^\w\s\-.,()]', '', name)  # remove special characters
    return name.strip()

# === Fetch Description ===
def fetch_description(cid):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            sections = data.get('Record', {}).get('Section', [])
            for section in sections:
                if section.get('TOCHeading') == "Names and Identifiers":
                    for subsection in section.get('Section', []):
                        if subsection.get('TOCHeading') == "Record Description":
                            return subsection['Information'][0]['Value']['StringWithMarkup'][0]['String']
    except:
        pass
    return 'Not Available'

def get_name_variations(compound_name):
    """Get different variations of the compound name to try."""
    variations = []
    
    # Original name
    variations.append(compound_name)
    
    # Cleaned name
    cleaned = clean_name(compound_name)
    if cleaned and cleaned != compound_name:
        variations.append(cleaned)
    
    # If original name contains semicolons, try all parts
    if ';' in compound_name:
        parts = [part.strip() for part in compound_name.split(';') if part.strip()]
        for part in parts:
            if part not in variations:
                variations.append(part)
            # Also try cleaned version of each part
            cleaned_part = clean_name(part)
            if cleaned_part and cleaned_part not in variations:
                variations.append(cleaned_part)
    
    return variations

def try_with_nih_cactus(compound_name):
    """Try to get synonyms using NIH Cactus service."""
    try:
        url = f"https://cactus.nci.nih.gov/chemical/structure/{compound_name}/names"
        response = requests.get(url, headers=headers, timeout=10)
        if response.ok:
            return [name.strip() for name in response.text.split('\n') if name.strip()]
    except Exception as e:
        print(f"Error in NIH Cactus for {compound_name}: {str(e)}")
    return []

def try_with_chembl(compound_name):
    """Try to get compound info from ChEMBL."""
    try:
        url = f"https://www.ebi.ac.uk/chembl/api/data/molecule?pref_name__iexact={compound_name}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.ok:
            data = response.json()
            if data['molecules']:
                molecule = data['molecules'][0]
                return {
                    'ChemSpiderId': molecule.get('chembl_id'),
                    'Synonyms': molecule.get('molecule_synonyms', []),
                    'Isomeric SMILES': molecule.get('molecule_structures', {}).get('canonical_smiles'),
                    'Calc. MW': molecule.get('molecule_properties', {}).get('full_mwt'),
                    'Source': 'ChEMBL'
                }
    except Exception as e:
        print(f"Error in ChEMBL for {compound_name}: {str(e)}")
    return None

def try_with_nci_resolver(compound_name):
    """Try to get compound info from NCI Chemical Identifier Resolver with proper URL structure."""
    try:
        # First try to get InChIKey directly
        inchikey_url = f"https://cactus.nci.nih.gov/chemical/structure/{compound_name}/stdinchikey"
        inchikey_response = requests.get(inchikey_url, headers=headers, timeout=10)
        
        if inchikey_response.ok:
            inchikey = inchikey_response.text.strip()
            if inchikey and inchikey != "N/A":
                # Try to find the compound in PubChem using the InChIKey
                time.sleep(PUBCHEM_DELAY)
                compounds = get_compounds(inchikey, 'inchikey')
                if compounds:
                    return extract_compound_data(compounds[0]), compound_name
        
        # If direct InChIKey lookup failed, try via SMILES
        smiles_url = f"https://cactus.nci.nih.gov/chemical/structure/{compound_name}/smiles"
        smiles_response = requests.get(smiles_url, headers=headers, timeout=10)
        
        if smiles_response.ok:
            smiles = smiles_response.text.strip()
            if smiles and smiles != "N/A":
                # Try to get InChIKey from the SMILES
                inchikey_url = f"https://cactus.nci.nih.gov/chemical/structure/{smiles}/stdinchikey"
                inchikey_response = requests.get(inchikey_url, headers=headers, timeout=10)
                
                inchikey = inchikey_response.text.strip() if inchikey_response.ok else None
                if inchikey and inchikey != "N/A":
                    # Try PubChem with InChIKey again
                    time.sleep(PUBCHEM_DELAY)
                    compounds = get_compounds(inchikey, 'inchikey')
                    if compounds:
                        return extract_compound_data(compounds[0]), compound_name
                
                # Try PubChem with SMILES directly
                time.sleep(PUBCHEM_DELAY)
                compounds = get_compounds(smiles, 'smiles')
                if compounds:
                    return extract_compound_data(compounds[0]), compound_name
                
                # If we have SMILES but couldn't find in PubChem, return the SMILES
                return {
                    'Isomeric SMILES': smiles,
                    'InChIKey': inchikey if inchikey else None,
                    'Source': 'NCI Resolver (SMILES only)'
                }, compound_name
    
    except Exception as e:
        print(f"Error in NCI Resolver for {compound_name}: {str(e)}")
    return None, None

def get_alternative_synonyms(compound_name, compound_formula):
    """Get synonyms from alternative sources when PubChem fails."""
    # Try NIH Cactus first
    synonyms = try_with_nih_cactus(compound_name)
    if synonyms:
        return synonyms[:MAX_SYNONYMS_TO_TRY]
    
    # If no synonyms from Cactus, try with formula
    if compound_formula:
        try:
            # Try to find compounds with the same formula in PubChem
            compounds = get_compounds(compound_formula, 'formula')
            if compounds:
                return [c.iupac_name for c in compounds[:MAX_SYNONYMS_TO_TRY] if c.iupac_name]
        except Exception as e:
            print(f"Error getting formula synonyms for {compound_name}: {str(e)}")
    
    return []

def extract_compound_data(compound):
    """Extract relevant data from PubChem Compound object."""
    synonyms = []
    try:
        synonyms = get_synonyms(compound.cid)[0]["Synonym"]
    except Exception as e:
        print(f"Error fetching synonyms for CID {compound.cid}: {str(e)}")
    
    # Get description using the fetch_description function
    description = fetch_description(compound.cid)
    
    return {
        'Formula': compound.molecular_formula,
        'Description': description,
        'Calc. MW': compound.molecular_weight,
        'PubChem CID': compound.cid,
        'IUPAC Name': compound.iupac_name,
        'Isomeric SMILES': compound.isomeric_smiles,
        'InChIKey': compound.inchikey,
        'Synonyms': synonyms,
        'Source': 'PubChem',
        'Structure': f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{compound.cid}/PNG'
    }

def fetch_compound_info(compound_name, compound_formula):
    """Fetch compound information with synonym fallback."""
    # Get different variations of the compound name
    name_variations = get_name_variations(compound_name)
    
    # Try each name variation
    for variation in name_variations:
        try:
            compounds = get_compounds(variation, 'name')
            if compounds:
                return extract_compound_data(compounds[0]), variation
            time.sleep(PUBCHEM_DELAY)
        except Exception as e:
            print(f"Error processing variation '{variation}': {str(e)}")
            continue

    # If no variations worked, try alternative sources for synonyms
    synonyms = get_alternative_synonyms(compound_name, compound_formula)

    for synonym in synonyms[:MAX_SYNONYMS_TO_TRY]:
        try:
            time.sleep(PUBCHEM_DELAY)
            compounds = get_compounds(synonym, 'name')
            if compounds:
                return extract_compound_data(compounds[0]), synonym
        except Exception as e:
            print(f"Error processing synonym '{synonym}': {str(e)}")
            continue

    # Try ChEMBL as a fallback
    chembl_data = try_with_chembl(compound_name)
    if chembl_data:
        return chembl_data, compound_name

    # Try NCI Resolver as a last resort - now returns both data and name
    nci_data, nci_name = try_with_nci_resolver(compound_name)
    if nci_data:
        return nci_data, nci_name

    return None, None

def process_excel_file(input_file, output_file, job_id=None, status_callback=None):
    """Process the Excel file to fetch compound information."""
    # Read the Excel file
    df = pd.read_excel(input_file)

    # Initialize new columns if they don't exist
    new_columns = [
        'PubChem CID', 'Synonyms', 'Isomeric SMILES', 
        'Description', 'Structure', 'Source', 'InChIKey', 'Formula', 
        'Calc. MW', 'IUPAC Name'
    ]
    for col in new_columns:
        if col not in df.columns:
            df[col] = None

    # Process each compound name
    total_rows = len(df)
    for idx, row in tqdm(df.iterrows(), total=total_rows, desc="Processing compounds"):
        compound_name = str(row['Name']).strip() if pd.notna(row['Name']) else None
        compound_formula = str(row['Formula']).strip() if pd.notna(row['Formula']) else None

        # Skip if already processed or no name
        if pd.notna(row.get('PubChem CID')) or not compound_name:
            continue

        # Fetch compound info
        compound_info, synonym_used = fetch_compound_info(compound_name, compound_formula)

        if compound_info:
            # Update the DataFrame with fetched info
            for key, value in compound_info.items():
                if key in df.columns:
                    df.at[idx, key] = value
        else:
            df.at[idx, 'Source'] = 'Not found in databases'

        # Update progress if callback is provided
        if status_callback and job_id:
            status_callback(job_id, idx + 1)
            
        # Sleep to avoid overloading servers
        time.sleep(PUBCHEM_DELAY)

    # Save the results to a new Excel file
    df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    input_file = input("Enter the path to your input Excel file: ").strip('"')
    output_file = input("Enter the path for the output Excel file: ").strip('"')

    print("\nStarting compound information fetching with synonym fallback...")
    process_excel_file(input_file, output_file)
    print("\nProcessing complete!")