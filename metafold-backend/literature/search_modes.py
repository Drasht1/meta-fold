from enum import Enum
from typing import List


class SearchMode(str, Enum):
    """
    Available literature search strategies.
    """

    STRICT = "strict"

    BALANCED = "balanced"

    BROAD = "broad"

    COMPREHENSIVE = "comprehensive"


def generate_queries(
    compound_name: str,
    iupac_name: str = "",
    synonyms: List[str] | None = None,
    mode: SearchMode = SearchMode.BALANCED
) -> List[str]:
    """
    Generate one or more PubMed queries depending
    on the selected search mode.

    Parameters
    ----------
    compound_name

    iupac_name

    synonyms

    mode

    Returns
    -------
    List[str]
    """

    if synonyms is None:
        synonyms = []

    queries = []

    # ---------------------------------------------------
    # STRICT
    # ---------------------------------------------------

    if mode == SearchMode.STRICT:

        queries.append(
            f'"{compound_name}"[Title/Abstract]'
        )

        return queries

    # ---------------------------------------------------
    # BALANCED
    # ---------------------------------------------------

    if mode == SearchMode.BALANCED:

        queries.append(compound_name)

        for synonym in synonyms[:5]:

            synonym = synonym.strip()

            if (
                synonym
                and synonym.lower() != compound_name.lower()
            ):
                queries.append(
                    f'"{synonym}"'
                )

        if (
            iupac_name
            and iupac_name.lower() != compound_name.lower()
        ):
            queries.append(
                f'"{iupac_name}"'
            )

        return queries

    # ---------------------------------------------------
    # BROAD
    # ---------------------------------------------------

    if mode == SearchMode.BROAD:

        queries.append(
            f'"{compound_name}"[All Fields]'
        )

        for synonym in synonyms[:10]:

            synonym = synonym.strip()

            if (
                synonym
                and synonym.lower() != compound_name.lower()
            ):
                queries.append(
                    f'"{synonym}"[All Fields]'
                )

        if (
            iupac_name
            and iupac_name.lower() != compound_name.lower()
        ):
            queries.append(
                f'"{iupac_name}"[All Fields]'
            )

        return queries

    # ---------------------------------------------------
    # COMPREHENSIVE
    # ---------------------------------------------------

    if mode == SearchMode.COMPREHENSIVE:

        queries.append(compound_name)

        queries.append(
            f'"{compound_name}"'
        )

        queries.append(
            f'"{compound_name}"[All Fields]'
        )

        queries.append(
            f'"{compound_name}"[Title/Abstract]'
        )

        if iupac_name:

            queries.append(
                f'"{iupac_name}"'
            )

            queries.append(
                f'"{iupac_name}"[All Fields]'
            )

        for synonym in synonyms:

            synonym = synonym.strip()

            if (
                synonym
                and synonym.lower() != compound_name.lower()
            ):

                queries.append(
                    f'"{synonym}"'
                )

                queries.append(
                    f'"{synonym}"[All Fields]'
                )

        # Remove duplicates while preserving order
        seen = set()

        unique = []

        for query in queries:

            if query not in seen:

                unique.append(query)

                seen.add(query)

        return unique

    return queries