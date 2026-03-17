# MetaFold

A modern web application for processing and analyzing chemical compound data from Excel files. MetaFold integrates with PubChem to fetch detailed compound information, clean and standardize chemical names, and provide comprehensive analysis tools.

## Features

- **Excel File Processing**: Upload and process Excel files containing chemical compound data
- **PubChem Integration**: Automatically fetch compound descriptions, properties, and identifiers from PubChem
- **Data Cleaning**: Intelligent cleaning and standardization of chemical compound names
- **Email Notifications**: Send processed results via email
- **Visit Tracking**: Built-in analytics for usage tracking
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **FastAPI Backend**: High-performance REST API with automatic documentation

## Tech Stack

### Frontend
- React 19
- Vite
- Tailwind CSS
- Lucide React (icons)

### Backend
- FastAPI
- Python 3.x
- MongoDB
- PubChemPy
- Pandas & NumPy
- Uvicorn

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (optional, for data persistence)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd metafold-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create `.env` file):
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   EMAIL_FROM=your-email@gmail.com
   MONGODB_URL=mongodb://localhost:27017/metafold  # Optional
   ```

5. Start the backend server:
   ```bash
   uvicorn app:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd metafold-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## Usage

1. Open the application in your browser
2. Upload an Excel file containing chemical compound data
3. The system will process the file, clean compound names, and fetch additional information from PubChem
4. Download the processed results or receive them via email

### API Endpoints

- `POST /upload`: Upload and process Excel files
- `GET /download/{file_id}`: Download processed results
- `POST /email`: Send results via email
- `POST /visits`: Track application visits
- `GET /docs`: API documentation (Swagger UI)

## Deployment

This application is configured for deployment on Render. The `render.yaml` file contains the deployment configuration.

### Environment Variables for Production
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_USERNAME`: Email username
- `EMAIL_PASSWORD`: Email password/app password
- `EMAIL_FROM`: Sender email address
- `MONGODB_URL`: MongoDB connection string (optional)

## Contributing

This application is configured for deployment on Render. The `render.yaml` file contains the deployment configuration.

### Environment Variables for Production
- `EMAIL_HOST`: SMTP server host
- `EMAIL_PORT`: SMTP server port
- `EMAIL_USERNAME`: Email username
- `EMAIL_PASSWORD`: Email password/app password
- `EMAIL_FROM`: Sender email address
- `MONGODB_URL`: MongoDB connection string (optional)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React code
- Write clear, concise commit messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) for providing comprehensive chemical compound data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [React](https://reactjs.org/) for the frontend library
- [Tailwind CSS](https://tailwindcss.com/) for utility-first CSS framework

## Support

If you encounter any issues or have questions, please open an issue on GitHub.