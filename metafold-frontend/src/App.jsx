import React, { useState, useEffect } from 'react';
import {
  Download, Eye
} from 'lucide-react';
// Main App component with state-based navigation
export default function App() {
  const [currentPage, setCurrentPage] = useState('landing');

  return (
    <div>
      {currentPage === 'landing' && <MetaFoldLanding setCurrentPage={setCurrentPage} />}
      {currentPage === 'processor' && <ChemicalCompoundProcessor setCurrentPage={setCurrentPage} />}
    </div>
  );
}

// Landing Page
function MetaFoldLanding({ setCurrentPage }) {
  const [isScrolled, setIsScrolled] = useState(false);


  const [visits, setVisits] = useState(0);
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  useEffect(() => {
    const fetchAndIncrementVisits = async () => {
      try {
        // Increment visit count
        const response = await fetch(`${API_BASE_URL}/visits`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        setVisits(data.count);
      } catch (error) {
        console.error('Error tracking visit:', error);
        // Fallback to show some number if API fails
        setVisits(0);
      }
    };

    fetchAndIncrementVisits();
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 overflow-x-hidden" style={{
      backgroundColor: '#0f1119',
      color: '#f5f5f0',
      fontFamily: 'Inter, sans-serif'
    }}>
      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-gray-900 bg-opacity-90 backdrop-blur-sm' : 'bg-transparent'
        }`}>
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-light text-blue-300">MetaFold</div>
          <div className="flex space-x-8">
            <button onClick={() => scrollToSection('features')} className="hover:text-blue-300 transition-colors">Features</button>
            <button onClick={() => scrollToSection('about')} className="hover:text-blue-300 transition-colors">About</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-purple-900 to-gray-900 opacity-20"></div>

          {/* Molecular Structures Animation */}
          <div className="absolute inset-0">
            {/* Molecule 1 */}
            <svg className="molecule-1 absolute opacity-15 animate-float" style={{
              top: '15%',
              left: '20%',
              animationDelay: '0.5s',
              animationDuration: '15s'
            }} width="100" height="100" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="10" fill="#70bbe0" />
              <circle cx="80" cy="30" r="7" fill="#70bbe0" />
              <circle cx="20" cy="70" r="7" fill="#70bbe0" />
              <circle cx="30" cy="20" r="7" fill="#70bbe0" />
              <circle cx="70" cy="80" r="7" fill="#70bbe0" />
              <line x1="50" y1="50" x2="80" y2="30" stroke="#70bbe0" strokeWidth="2" />
              <line x1="50" y1="50" x2="20" y2="70" stroke="#70bbe0" strokeWidth="2" />
              <line x1="50" y1="50" x2="30" y2="20" stroke="#70bbe0" strokeWidth="2" />
              <line x1="50" y1="50" x2="70" y2="80" stroke="#70bbe0" strokeWidth="2" />
            </svg>

            {/* Molecule 2 */}
            <svg className="molecule-2 absolute opacity-15 animate-float" style={{
              bottom: '20%',
              right: '25%',
              animationDelay: '1s',
              animationDuration: '18s'
            }} width="120" height="120" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="12" fill="#70bbe0" />
              <circle cx="30" cy="30" r="8" fill="#70bbe0" />
              <circle cx="90" cy="30" r="8" fill="#70bbe0" />
              <circle cx="90" cy="90" r="8" fill="#70bbe0" />
              <circle cx="30" cy="90" r="8" fill="#70bbe0" />
              <line x1="60" y1="60" x2="30" y2="30" stroke="#70bbe0" strokeWidth="2" />
              <line x1="60" y1="60" x2="90" y2="30" stroke="#70bbe0" strokeWidth="2" />
              <line x1="60" y1="60" x2="90" y2="90" stroke="#70bbe0" strokeWidth="2" />
              <line x1="60" y1="60" x2="30" y2="90" stroke="#70bbe0" strokeWidth="2" />
              <line x1="30" y1="30" x2="90" y2="30" stroke="#70bbe0" strokeWidth="2" />
              <line x1="90" y1="30" x2="90" y2="90" stroke="#70bbe0" strokeWidth="2" />
              <line x1="90" y1="90" x2="30" y2="90" stroke="#70bbe0" strokeWidth="2" />
              <line x1="30" y1="90" x2="30" y2="30" stroke="#70bbe0" strokeWidth="2" />
            </svg>

            {/* Molecule 3 */}
            <svg className="molecule-3 absolute opacity-15 animate-float" style={{
              bottom: '30%',
              left: '15%',
              animationDelay: '1.5s',
              animationDuration: '20s'
            }} width="80" height="80" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r="8" fill="#70bbe0" />
              <circle cx="40" cy="10" r="6" fill="#70bbe0" />
              <circle cx="65" cy="55" r="6" fill="#70bbe0" />
              <circle cx="15" cy="55" r="6" fill="#70bbe0" />
              <line x1="40" y1="40" x2="40" y2="10" stroke="#70bbe0" strokeWidth="2" />
              <line x1="40" y1="40" x2="65" y2="55" stroke="#70bbe0" strokeWidth="2" />
              <line x1="40" y1="40" x2="15" y2="55" stroke="#70bbe0" strokeWidth="2" />
              <line x1="65" y1="55" x2="15" y2="55" stroke="#70bbe0" strokeWidth="2" />
            </svg>

            {/* Molecule 4 */}
            <svg className="molecule-4 absolute opacity-15 animate-float" style={{
              top: '25%',
              right: '15%',
              animationDelay: '2s',
              animationDuration: '16s'
            }} width="90" height="90" viewBox="0 0 90 90">
              <circle cx="45" cy="45" r="9" fill="#70bbe0" />
              <circle cx="45" cy="15" r="7" fill="#70bbe0" />
              <circle cx="45" cy="75" r="7" fill="#70bbe0" />
              <circle cx="15" cy="45" r="7" fill="#70bbe0" />
              <circle cx="75" cy="45" r="7" fill="#70bbe0" />
              <line x1="45" y1="45" x2="45" y2="15" stroke="#70bbe0" strokeWidth="2" />
              <line x1="45" y1="45" x2="45" y2="75" stroke="#70bbe0" strokeWidth="2" />
              <line x1="45" y1="45" x2="15" y2="45" stroke="#70bbe0" strokeWidth="2" />
              <line x1="45" y1="45" x2="75" y2="45" stroke="#70bbe0" strokeWidth="2" />
            </svg>
          </div>
        </div>

        <div className="relative z-10 text-center max-w-4xl mx-auto">

          <h1 className="text-6xl md:text-8xl font-light mb-6 tracking-tight bg-gradient-to-r from-blue-300 via-purple-300 to-cyan-300 bg-clip-text text-transparent animate-pulse">
            Meta<span className="text-blue-300">Fold</span>
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Advanced metabolite data processing and analysis platform. Transform complex molecular data into actionable insights.
          </p>
          <button
            onClick={() => setCurrentPage('processor')}
            className="group mt-12 px-8 py-4 border-2 border-blue-300 border-opacity-40 rounded-full text-sm tracking-wide hover:bg-blue-300 hover:bg-opacity-20 hover:border-opacity-60 transition-all duration-500 relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-300 to-purple-300 opacity-0 group-hover:opacity-10 rounded-full transition-opacity duration-500"></div>
            <span className="relative z-10 font-medium">Start Processing</span>
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6 relative">
        {/* Background Animation */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="absolute w-32 h-32 border border-blue-300 border-opacity-5 rounded-full animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${i * 0.5}s`,
                animationDuration: `${4 + Math.random() * 2}s`
              }}
            />
          ))}
        </div>

        <div className="container mx-auto max-w-6xl relative z-10">
          <h2 className="text-4xl font-light text-center mb-16 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
            Metabolomics Features
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="group text-center p-8 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 bg-opacity-60 backdrop-blur-sm border border-blue-300 border-opacity-10 hover:border-opacity-30 transition-all duration-500 hover:transform hover:scale-105">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-blue-300 to-purple-300 bg-opacity-20 rounded-full flex items-center justify-center group-hover:animate-spin transition-all duration-500">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full flex items-center justify-center">
                  <span className="text-xl">🧬</span>
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Metabolite Identification
              </h3>
              <p className="text-gray-300">Advanced molecular structure analysis and metabolite compound identification using mass spectrometry data</p>
            </div>

            <div className="group text-center p-8 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 bg-opacity-60 backdrop-blur-sm border border-blue-300 border-opacity-10 hover:border-opacity-30 transition-all duration-500 hover:transform hover:scale-105">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-green-300 to-blue-300 bg-opacity-20 rounded-full flex items-center justify-center group-hover:animate-pulse transition-all duration-500">
                <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-blue-400 rounded-full flex items-center justify-center">
                  <span className="text-xl">📊</span>
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-4 bg-gradient-to-r from-green-300 to-blue-300 bg-clip-text text-transparent">
                Statistical Analysis & Visualization
              </h3>
              <p className="text-gray-300">Apply statistical methods for comprehensive data analysis and interpretation, leveraging chemical databases such as PubChem, ChEMBL, and NIH Cactus. Generate interactive visualizations and comprehensive reports to effectively communicate compound properties, structural insights, and molecular relationships.</p>
            </div>

            <div className="group text-center p-8 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 bg-opacity-60 backdrop-blur-sm border border-blue-300 border-opacity-10 hover:border-opacity-30 transition-all duration-500 hover:transform hover:scale-105">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-purple-300 to-pink-300 bg-opacity-20 rounded-full flex items-center justify-center group-hover:animate-bounce transition-all duration-500">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                  <span className="text-xl">⚡</span>
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-4 bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                Export File Report
              </h3>
              <p className="text-gray-300">Get accurate metabolomics results in seconds with our accelerated processing algorithms, seamlessly exported into structured Excel reports for immediate analysis and interpretation</p>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-6 bg-gradient-to-br from-gray-800 to-gray-900 bg-opacity-50 backdrop-blur-sm relative overflow-hidden">
        {/* Animated Molecular Structure Background */}
        <div className="absolute inset-0 opacity-5">
          <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="metabolitePattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
                <circle cx="50" cy="50" r="20" fill="none" stroke="#70bbe0" strokeWidth="1" opacity="0.3" />
                <circle cx="20" cy="20" r="8" fill="#70bbe0" opacity="0.2" />
                <circle cx="80" cy="80" r="8" fill="#46769B" opacity="0.2" />
                <line x1="20" y1="20" x2="50" y2="50" stroke="#70bbe0" strokeWidth="1" opacity="0.2" />
                <line x1="50" y1="50" x2="80" y2="80" stroke="#46769B" strokeWidth="1" opacity="0.2" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#metabolitePattern)" />
          </svg>
        </div>

        <div className="container mx-auto max-w-4xl text-center relative z-10">
          <div className="mb-8">
            {/* Animated Metabolite Icon */}
            <div className="inline-flex items-center justify-center w-16 h-16 mx-auto mb-6 relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-300 to-purple-300 rounded-full animate-pulse opacity-20"></div>
              <div className="relative z-10 text-3xl">🧪</div>
            </div>
          </div>

          <h2 className="text-4xl font-light  bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
            About MetaFold
          </h2>
          <div className='flex items-center m-auto my-6 justify-center'>
              <Eye className="w-8 h-8 text-white mr-2" />
              <span className="text-xl text-white font-medium">
                {visits} visits
              </span>
            </div>
          <div className="text-lg text-gray-300 leading-relaxed space-y-4">
            <p>
              MetaFold is a powerful computational platform designed to process, analyze, and visualize complex metabolite data from various biological sources. We bridge the gap between raw metabolomic data and meaningful scientific insights.
            </p>
            <p className="text-blue-300 font-medium">
              Transforming metabolomics research through intelligent automation and precision analytics.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-gray-700 relative">
        {/* Subtle molecular animation in footer */}
        <div className="absolute inset-0 overflow-hidden opacity-5">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="absolute w-8 h-8 border border-blue-300 rounded-full animate-pulse"
              style={{
                left: `${20 + i * 30}%`,
                top: '50%',
                animationDelay: `${i * 0.5}s`,
                animationDuration: '3s'
              }}
            />
          ))}
        </div>
        <div className="container mx-auto text-center relative z-10">

          <div className="flex justify-center items-center space-x-2">
            <p className="bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
              MetaFold © {new Date().getFullYear()} - Advancing Metabolomics Research
            </p>
            
          </div>
        </div>
      </footer>
    </div>
  );
}



function ChemicalCompoundProcessor({ setCurrentPage }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [currentJobId, setCurrentJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null);
  const [selectedColumns, setSelectedColumns] = useState([
    "Name",
    "Formula",
    "Calc. MW",
    "m/z",
    "RT [min]",
    "Area (Max.)"
  ]);
  const [showColumnSelector, setShowColumnSelector] = useState(false);
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const [email, setEmail] = useState('');
  // Enhanced color palette with gradients
  const colors = {
    primary: '#70bbe0',
    secondary: '#46769B',
    tertiary: '#2F5F8A',
    light: '#1a2836',
    dark: '#0f1119',
    white: '#f5f5f0',
    gray: '#6b7280',
    accent: '#a855f7'
  };

  // Define all possible columns
  const allColumns = [
    "Name",
    "Formula",
    "Calc. MW",
    "m/z",
    "RT [min]",
    "Area (Max.)",
    "PubChem CID",
    "IUPAC Name",
    "Isomeric SMILES",
    "Description",
    "Source"
  ];

  const [visits, setVisits] = useState(0);

  useEffect(() => {
    const fetchAndIncrementVisits = async () => {
      try {
        // Increment visit count
        const response = await fetch(`${API_BASE_URL}/visits`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        setVisits(data.count);
      } catch (error) {
        console.error('Error tracking visit:', error);
        // Fallback to show some number if API fails
        setVisits(0);
      }
    };

    fetchAndIncrementVisits();
  }, []);

  useEffect(() => {
    fetchJobs();
    // Poll for job updates every 5 seconds
    const interval = setInterval(() => {
      if (currentJobId) {
        fetchJobStatus(currentJobId);
      }
      fetchJobs();
    }, 5000);

    return () => clearInterval(interval);
  }, [currentJobId]);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (error && error.includes('email')) {
      setError(null);
    }
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // Fetch all processing jobs
  const fetchJobs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/jobs`);
      if (response.ok) {
        const data = await response.json();
        setJobs(data.sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at)));
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  };

  // Fetch status of a specific job
  const fetchJobStatus = async (jobId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/status/${jobId}`);
      if (response.ok) {
        const data = await response.json();
        setJobStatus(data);

        // Fetch results when job is completed using the correct endpoint
        if (data.status === 'completed') {
          await fetchPreviewData(jobId);
        }
      }
    } catch (err) {
      console.error('Error fetching job status:', err);
    }
  };

  // Fetch preview data for a specific job (using original endpoint)
  const fetchPreviewData = async (jobId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/preview/${jobId}?limit=10000`);
      if (response.ok) {
        const data = await response.json();
        // Handle both array format and object with data property
        if (Array.isArray(data)) {
          setPreviewData(data);
        } else if (data.data && Array.isArray(data.data)) {
          setPreviewData(data.data);
        } else if (data.results && Array.isArray(data.results)) {
          setPreviewData(data.results);
        } else {
          setPreviewData(data);
        }
      } else {
        console.error('Failed to fetch preview data');
      }
    } catch (err) {
      console.error('Error fetching preview data:', err);
      setError('Failed to load preview data. Please try again.');
    }
  };

  // Handle file selection with validation
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && (selectedFile.name.endsWith('.xlsx') || selectedFile.name.endsWith('.xls'))) {
      setFile(selectedFile);
      setError(null);
    } else {
      setFile(null);
      setError('Please select a valid Excel file (.xlsx or .xls)');
    }
  };

  const handleResumeJob = async (jobId) => {
    try {
      setError(null);
      const response = await fetch(`${API_BASE_URL}/resume/${jobId}`, {
        method: 'POST',
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentJobId(jobId);
        setJobStatus({
          status: 'processing',
          progress: 0,
          progress_percent: 0
        });
        fetchJobStatus(jobId);
        fetchJobs();
        setError(`Job resumed successfully! Recovery attempt #${data.recovery_count}`);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to resume job');
      }
    } catch (err) {
      console.error('Error resuming job:', err);
      setError('Server error. Could not resume job.');
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }
    if (!email || !validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setUploading(true);
    setError(null);
    setPreviewData(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('email', email);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentJobId(data.job_id);
        setJobStatus({
          status: 'processing',
          progress: 0,
          progress_percent: 0
        });
        fetchJobStatus(data.job_id);
        fetchJobs();
        setFile(null);
        setEmail('');
        setError('File uploaded successfully! You will receive an email with results.');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Upload failed');
      }
    } catch (err) {
      console.error('Error uploading file:', err);
      setError('Server error. Please try again later.');
    } finally {
      setUploading(false);
    }
  };
  // Handle download of processed file
  const handleDownload = (jobId) => {
    window.open(`${API_BASE_URL}/download/${jobId}`, '_blank');
  };

  // Handle job selection from history
  const selectJob = async (jobId) => {
    setCurrentJobId(jobId);
    setPreviewData(null);
    await fetchJobStatus(jobId);
    // Also fetch results if job is completed
    const job = jobs.find(j => j.id === jobId);
    if (job && job.status === 'completed') {
      await fetchPreviewData(jobId);
    }
  };

  // Format date string
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  // Toggle row expansion for viewing compound details
  const toggleRowExpansion = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  // Toggle column selection modal
  const toggleColumnSelector = () => {
    setShowColumnSelector(!showColumnSelector);
  };

  // Handle column selection change with validation
  const handleColumnToggle = (column) => {
    if (selectedColumns.includes(column)) {
      if (selectedColumns.length > 1) { // Ensure at least one column is selected
        setSelectedColumns(selectedColumns.filter(col => col !== column));
      }
    } else {
      setSelectedColumns([...selectedColumns, column]);
    }
  };

  // Alternative toggle column function (simpler version)
  const toggleColumn = (column) => {
    setSelectedColumns(prev =>
      prev.includes(column)
        ? prev.filter(col => col !== column)
        : [...prev, column]
    );
  };

  // Get PubChem image URL for a CID
  const getPubChemImageUrl = (cid) => {
    return cid ? `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${cid}/PNG` : null;
  };

  // DEMO: Add sample data for testing
  const loadSampleData = () => {
    const sampleData = [
      {
        "Name": "Glucose",
        "Formula": "C6H12O6",
        "Calc. MW": "180.16",
        "m/z": "181.07",
        "RT [min]": "2.45",
        "Area (Max.)": "1234567",
        "PubChem CID": "5793",
        "IUPAC Name": "D-glucose",
        "Description": "A simple sugar"
      },
      {
        "Name": "Caffeine",
        "Formula": "C8H10N4O2",
        "Calc. MW": "194.19",
        "m/z": "195.09",
        "RT [min]": "5.23",
        "Area (Max.)": "987654",
        "PubChem CID": "2519",
        "IUPAC Name": "1,3,7-trimethylpurine-2,6-dione",
        "Description": "A central nervous system stimulant"
      },
      {
        "Name": "Aspirin",
        "Formula": "C9H8O4",
        "Calc. MW": "180.16",
        "m/z": "181.07",
        "RT [min]": "8.91",
        "Area (Max.)": "567890",
        "PubChem CID": "2244",
        "IUPAC Name": "2-acetoxybenzoic acid",
        "Description": "Nonsteroidal anti-inflammatory drug"
      }
    ];
    setPreviewData(sampleData);
    setJobStatus({
      status: 'completed',
      progress: 100,
      progress_percent: 100
    });
  };

  return (
    <div className="flex flex-col min-h-screen relative overflow-hidden" style={{ backgroundColor: colors.dark, color: colors.white }}>
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-blue-300 rounded-full opacity-20 animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 2}s`
            }}
          />
        ))}
      </div>

      {/* Header */}
      <header className="relative z-10 text-white shadow-lg border-b border-gray-700 backdrop-blur-sm" style={{ backgroundColor: `${colors.dark}dd` }}>
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <button
            onClick={() => setCurrentPage('landing')}
            className="text-3xl font-light bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300"
          >
            MetaFold
          </button>
          <nav className="flex space-x-6">
            <button onClick={() => setCurrentPage('landing')} className="hover:text-blue-300 transition-colors duration-300 hover:scale-105">Home</button>
            <button onClick={() => setCurrentPage('processor')} className="text-blue-300 font-medium">Processor</button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 flex-grow relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column - Upload & Job Status */}
          <div className="lg:col-span-3 space-y-6">
            {/* File Upload Card */}
            <div className="group p-6 rounded-xl backdrop-blur-sm border hover:border-opacity-40 transition-all duration-500 hover:transform hover:scale-[1.02]"
              style={{
                backgroundColor: `${colors.light}cc`,
                border: '1px solid rgba(112, 187, 224, 0.2)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
              }}>
              <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Upload Metabolomics Data
              </h2>

              <div className="space-y-4">
                {/* Email Input */}
                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={handleEmailChange}
                    placeholder="Enter your email"
                    className="w-full p-4 rounded-lg border-2 border-gray-600 bg-gray-800 bg-opacity-60 text-white backdrop-blur-sm hover:border-blue-400 transition-all duration-300 focus:border-blue-300 focus:ring-2 focus:ring-blue-300 focus:ring-opacity-20"
                    required
                  />
                  <div className="absolute right-3 top-3 text-blue-300 opacity-60">
                    ✉️
                  </div>
                </div>

                {/* File Input */}
                <div className="relative">
                  <input
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileChange}
                    className="w-full p-4 rounded-lg border-2 border-gray-600 bg-gray-800 bg-opacity-60 text-white backdrop-blur-sm hover:border-blue-400 transition-all duration-300 focus:border-blue-300 focus:ring-2 focus:ring-blue-300 focus:ring-opacity-20"
                  />
                  <div className="absolute right-3 top-3 text-blue-300 opacity-60">
                    📁
                  </div>
                </div>

                {file && (
                  <div className="text-sm text-gray-300 p-3 bg-gray-800 bg-opacity-40 rounded-lg border border-gray-600 animate-pulse">
                    <span className="text-blue-300">📄</span> Selected: {file.name}
                  </div>
                )}

                <button
                  onClick={handleUpload}
                  disabled={!file || !email || uploading}
                  className="group w-full py-4 px-6 rounded-lg text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-500 relative overflow-hidden hover:scale-105"
                  style={{
                    background: uploading
                      ? colors.gray
                      : 'linear-gradient(135deg, #70bbe0 0%, #46769B 100%)',
                    boxShadow: uploading ? 'none' : '0 4px 20px rgba(112, 187, 224, 0.3)'
                  }}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-300 to-blue-300 opacity-0 group-hover:opacity-20 rounded-lg transition-opacity duration-500"></div>
                  <span className="relative z-10">
                    {uploading ? (
                      <span className="flex items-center justify-center">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                        Processing...
                      </span>
                    ) : (
                      'Upload & Analyze'
                    )}
                  </span>
                </button>

                {/* DEMO BUTTON */}
                <button
                  onClick={loadSampleData}
                  className="w-full py-3 px-4 rounded-lg border-2 border-purple-300 border-opacity-40 text-purple-300 hover:bg-purple-300 hover:bg-opacity-10 transition-all duration-300 text-sm"
                >
                  Load Sample Data (Demo)
                </button>

                {error && (
                  <div className={`text-sm mt-2 p-3 rounded-lg border border-opacity-30 animate-pulse ${error.includes('successfully') ? 'text-green-400 bg-green-900 bg-opacity-20 border-green-600' : 'text-red-400 bg-red-900 bg-opacity-20 border-red-600'}`}>
                    {error.includes('successfully') ? '✅' : '⚠'} {error}
                  </div>
                )}
              </div>
            </div>

            {/* Job Status Card */}
            <div className="p-6 rounded-xl backdrop-blur-sm border transition-all duration-500 hover:transform hover:scale-[1.02]"
              style={{
                backgroundColor: `${colors.light}cc`,
                border: '1px solid rgba(112, 187, 224, 0.2)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
              }}>
              <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Recent Jobs
              </h2>

              <div className="space-y-3">
                {jobs.length > 0 ? jobs.map(job => (
                  <div
                    key={job.id}
                    className="p-4 rounded-lg border border-gray-600 bg-gray-800 bg-opacity-60 hover:bg-opacity-80 transition-all duration-300 cursor-pointer"
                    onClick={() => selectJob(job.id)}
                  >
                    <div className="text-sm font-medium text-white">{job.filename}</div>
                    <div className="text-xs text-gray-400 flex items-center mt-1">
                      <span className={`inline-block w-2 h-2 rounded-full mr-2 ${job.status === 'completed' ? 'bg-green-400' : job.status === 'failed' ? 'bg-red-400' : 'bg-yellow-400'}`}></span>
                      Status: {job.status}
                    </div>
                    <div className="text-xs text-gray-400">
                      {new Date(job.created_at || job.uploaded_at).toLocaleString()}
                    </div>
                    {(job.status === 'failed' || job.status === 'cancelled') && job.can_resume && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // Prevent job selection
                          handleResumeJob(job.id);
                        }}
                        className="mt-2 px-3 py-1 text-xs bg-yellow-600 hover:bg-yellow-500 text-white rounded transition-colors"
                      >
                        Resume Job
                      </button>
                    )}
                  </div>
                )) : (
                  <div className="text-center text-gray-400 py-4">
                    <div className="text-3xl mb-2">📋</div>
                    <p className="text-sm">No jobs yet</p>
                  </div>
                )}
              </div>
            </div>

            {/* Column Selector */}
            <div className="p-6 rounded-xl backdrop-blur-sm border transition-all duration-500 hover:transform hover:scale-[1.02]"
              style={{
                backgroundColor: `${colors.light}cc`,
                border: '1px solid rgba(112, 187, 224, 0.2)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
              }}>
              <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Column Selector
              </h2>

              <div className="space-y-2 max-h-64 overflow-y-auto">
                {allColumns.map(column => (
                  <label key={column} className="flex items-center space-x-2 text-sm hover:text-blue-300 transition-colors duration-300 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedColumns.includes(column)}
                      onChange={() => toggleColumn(column)}
                      className="rounded border-gray-600 bg-gray-800 text-blue-500 focus:ring-blue-500"
                    />
                    <span>{column}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Data Preview */}
          <div className="lg:col-span-9">
            <div className="p-6 rounded-xl backdrop-blur-sm border transition-all duration-500"
              style={{
                backgroundColor: `${colors.light}cc`,
                border: '1px solid rgba(112, 187, 224, 0.2)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
              }}>
              <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Data Preview
              </h2>

              {previewData && Array.isArray(previewData) && previewData.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-gray-600">
                        {selectedColumns.map(column => (
                          <th key={column} className="text-left p-3 font-medium bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                            {column}
                          </th>
                        ))}
                        <th className="p-3"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {previewData.map((row, rowIndex) => (
                        <React.Fragment key={rowIndex}>
                          <tr
                            className={`border-b border-gray-700 hover:bg-gray-800 hover:bg-opacity-50 transition-colors duration-300 cursor-pointer ${expandedRow === rowIndex ? 'bg-gray-800 bg-opacity-30' : ''}`}
                            onClick={() => setExpandedRow(expandedRow === rowIndex ? null : rowIndex)}
                          >
                            {selectedColumns.map(column => (
                              <td key={`${rowIndex}-${column}`} className="p-3">
                                {row[column] || '-'}
                              </td>
                            ))}
                            <td className="p-3 text-right">
                              <button className="text-blue-300 hover:text-purple-300 transition-colors">
                                {expandedRow === rowIndex ? '▲' : '▼'}
                              </button>
                            </td>
                          </tr>
                          {expandedRow === rowIndex && (
                            <tr className="border-b border-gray-700 bg-gray-800 bg-opacity-20">
                              <td colSpan={selectedColumns.length + 1} className="p-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                  <div>
                                    <h3 className="text-sm font-medium mb-2 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                                      Molecular Properties
                                    </h3>
                                    <div className="grid grid-cols-2 gap-2 text-xs">
                                      {Object.entries(row).filter(([key]) => !selectedColumns.includes(key) && row[key]).map(([key, value]) => (
                                        <div key={key} className="p-2 bg-gray-800 bg-opacity-40 rounded">
                                          <div className="text-gray-400">{key}</div>
                                          <div className="text-white">
                                            {key === 'PubChem CID' ? (
                                              <a
                                                href={`https://pubchem.ncbi.nlm.nih.gov/compound/${value}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-400 hover:text-blue-300 underline cursor-pointer"
                                              >
                                                {value}
                                              </a>
                                            ) : (
                                              value || '-'
                                            )}
                                          </div>
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                  <div>
                                    <h3 className="text-sm font-medium mb-2 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                                      Molecular Structure
                                    </h3>
                                    <div className="bg-gray-800 bg-opacity-40 rounded-lg p-4 flex items-center justify-center h-full">
                                      {row['PubChem CID'] ? (
                                        <img
                                          src={getPubChemImageUrl(row['PubChem CID'])}
                                          alt={`Structure of ${row['Name'] || 'compound'}`}
                                          className="max-w-full h-auto rounded"
                                          onError={(e) => {
                                            e.target.style.display = 'none';
                                            e.target.nextSibling.style.display = 'block';
                                          }}
                                        />
                                      ) : null}
                                      <div className="text-center" style={{ display: row['PubChem CID'] ? 'none' : 'block' }}>
                                        <div className="text-5xl mb-2">🧪</div>
                                        <div className="text-xs text-gray-400">Structure visualization</div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </td>
                            </tr>
                          )}
                        </React.Fragment>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-16 text-gray-400">
                  <div className="text-6xl mb-4">📊</div>
                  <p className="text-lg mb-2">No data to display</p>
                  <p className="text-sm">Upload a file to begin processing or click "Load Sample Data" to test</p>
                </div>
              )}

              {previewData && Array.isArray(previewData) && previewData.length > 0 && (
                <div className="mt-6 flex justify-between items-center">
                  <div className="text-sm text-gray-400">
                    Showing {previewData.length} compounds
                  </div>
                  <div className="flex space-x-2">
                    <button
                      className="px-4 py-2 rounded-lg border border-blue-300 border-opacity-40 text-blue-300 hover:bg-blue-300 hover:bg-opacity-10 transition-colors"
                      onClick={() => {
                        if (currentJobId) {
                          handleDownload(currentJobId);
                        } else {
                          alert('No job available for download');
                        }
                      }}
                    >
                      Export to Excel
                    </button>

                  </div>
                </div>
              )}
            </div>

            {/* Job Status Indicator */}
            {jobStatus && (
              <div className="mt-6 p-6 rounded-xl backdrop-blur-sm border transition-all duration-500"
                style={{
                  backgroundColor: `${colors.light}cc`,
                  border: '1px solid rgba(112, 187, 224, 0.2)',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
                }}>
                <h2 className="text-xl font-semibold mb-4 bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                  Processing Status
                </h2>

                <div className="space-y-4">
                  <div className="flex justify-between text-sm">
                    <span>Job ID: {currentJobId || 'demo'}</span>
                    <span className={`font-medium ${jobStatus.status === 'completed' ? 'text-green-400' :
                      jobStatus.status === 'failed' ? 'text-red-400' :
                        'text-blue-400'
                      }`}>
                      {jobStatus.status.charAt(0).toUpperCase() + jobStatus.status.slice(1)}
                    </span>
                  </div>

                  <div className="w-full bg-gray-700 rounded-full h-2.5">
                    <div
                      className="bg-gradient-to-r from-blue-300 to-purple-300 h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${jobStatus.progress_percent || jobStatus.progress || 0}%` }}
                    ></div>
                  </div>

                  <div className="text-sm text-gray-400">
                    {jobStatus.status === 'completed' ? (
                      'Analysis complete! Results are ready and have been sent to your email.'
                    ) : jobStatus.status === 'failed' ? (
                      'Processing failed. Please try again or check your email for details.'
                    ) : (
                      `Processing... ${jobStatus.progress_percent || jobStatus.progress || 0}% complete`
                    )}
                  </div>

                  {jobStatus.status === 'completed' && currentJobId && (
                    <button
                      className="w-full mt-4 py-2 px-4 rounded-lg bg-gradient-to-r from-green-400 to-blue-400 text-gray-900 font-medium hover:opacity-90 transition-opacity"
                      onClick={() => handleDownload(currentJobId)}
                    >
                      <Download size={18} className="inline mr-2" />
                      Download Processed File
                    </button>
                  )}

                  {jobStatus.status === 'failed' && jobStatus.can_resume && (
                    <button
                      className="w-full mt-2 py-2 px-4 rounded-lg bg-gradient-to-r from-yellow-400 to-orange-400 text-gray-900 font-medium hover:opacity-90 transition-opacity"
                      onClick={() => handleResumeJob(currentJobId)}
                    >
                      🔄 Resume Processing
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-6 px-4 border-t border-gray-700 relative z-10">
        <div className="container mx-auto text-center">
          <div className="flex justify-center items-center space-x-2">
            <p className="bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
              MetaFold © {new Date().getFullYear()} - Advancing Metabolomics Research
            </p>
            <div className='flex items-center ml-10'>
              <Eye className="w-4 h-4 text-white mr-2" />
              <span className="text-sm text-white font-medium">
                {visits} visits
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
