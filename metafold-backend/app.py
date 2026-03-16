from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr
import pandas as pd
import uuid
import os
import time
from typing import List, Dict, Any, Optional
import shutil
import uvicorn
from datetime import datetime
from compound_processor import process_excel_file 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MetaFold API", description="API for processing Excel files with MetaFold")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
# Email configuration (set these as environment variables in production)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")  # Your email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # Your app password
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USERNAME)

# Create directories for storing files
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# MongoDB Atlas connection
MONGO_URL = os.getenv("MONGODB_URL", "")
client = MongoClient(MONGO_URL)
db = client.website_stats
visits_collection = db.visits

class VisitResponse(BaseModel):
    count: int

# Store job statuses in memory (for a production app, use a database)
jobs = {}

class JobStatus(BaseModel):
    id: str
    status: str
    filename: str
    user_email: str
    uploaded_at: str
    completed_at: Optional[str] = None
    processed_rows: int = 0
    total_rows: int = 0
    error: Optional[str] = None

class UploadRequest(BaseModel):
    email: EmailStr

def send_email(to_email: str, subject: str, body: str, attachment_path: Optional[str] = None):
    """Send email notification"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Create SMTP session
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()  # Enable TLS encryption
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, to_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        raise e

@app.post("/api/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    email: str = Form(...)
):
    # Validate email format
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Valid email address is required")
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are accepted")
    
    # Validate email configuration
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        raise HTTPException(
            status_code=500, 
            detail="Email service not configured. Please contact administrator."
        )
    
    # Generate unique ID for the job
    job_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save uploaded file
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    output_path = os.path.join(PROCESSED_DIR, f"{job_id}_processed_{file.filename}")
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create job status
    jobs[job_id] = JobStatus(
        id=job_id,
        status="pending",
        filename=file.filename,
        user_email=email,
        uploaded_at=datetime.now().isoformat(),
    )
    
    # Send confirmation email
    try:
        confirmation_subject = "MetaFold Processing Started"
        confirmation_body = f"""
        <html>
        <body>
            <h2>MetaFold Processing Started</h2>
            <p>Hello,</p>
            <p>Your file <strong>{file.filename}</strong> has been uploaded successfully and processing has started.</p>
            <p><strong>Job ID:</strong> {job_id}</p>
            <p><strong>Uploaded at:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>You will receive another email when the processing is complete.</p>
            <br>
            <p>Best regards,<br>MetaFold Team</p>
        </body>
        </html>
        """
        background_tasks.add_task(send_email, email, confirmation_subject, confirmation_body)
    except Exception as e:
        logger.warning(f"Could not send confirmation email: {e}")
    
    # Process the file in the background
    background_tasks.add_task(process_file_task, job_id, input_path, output_path)
    
    return {"job_id": job_id, "status": "File uploaded successfully, processing started"}

def process_file_task(job_id: str, input_path: str, output_path: str):
    """Background task to process the Excel file"""
    jobs[job_id].status = "processing"
    
    try:
        # Get total rows for progress tracking
        df = pd.read_excel(input_path)
        jobs[job_id].total_rows = len(df)
        
        # Process the file using imported function
        process_excel_file(input_path, output_path, job_id=job_id, status_callback=update_job_status)
        
        # Update job status
        jobs[job_id].status = "completed"
        jobs[job_id].completed_at = datetime.now().isoformat()
        jobs[job_id].processed_rows = jobs[job_id].total_rows
        
        # Send completion email
        send_completion_email(job_id, output_path)
        
    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)
        logger.error(f"Error processing file: {e}")
        
        # Send failure email
        send_failure_email(job_id, str(e))

def send_completion_email(job_id: str, output_path: str):
    """Send email notification when processing is complete"""
    job = jobs[job_id]
    
    subject = f"MetaFold Processing Complete - {job.filename}"
    body = f"""
    <html>
    <body>
        <h2>MetaFold Processing Complete!</h2>
        <p>Hello,</p>
        <p>Great news! Your file processing has been completed successfully.</p>
        
        <h3>Processing Details:</h3>
        <ul>
            <li><strong>Job ID:</strong> {job.id}</li>
            <li><strong>Original File:</strong> {job.filename}</li>
            <li><strong>Uploaded:</strong> {job.uploaded_at}</li>
            <li><strong>Completed:</strong> {job.completed_at}</li>
            <li><strong>Rows Processed:</strong> {job.processed_rows:,}</li>
        </ul>
        
        <p>Your processed file is ready for download. You can download it using the following methods:</p>
        
        <h3>Download Options:</h3>
        <ol>
            <li><strong>Direct Download:</strong> Visit our API endpoint:<br>
                <code>GET /api/download/{job_id}</code>
            </li>
            <li><strong>Preview Data:</strong> Check a preview of your processed data:<br>
                <code>GET /api/preview/{job_id}</code>
            </li>
        </ol>
        
        <p><strong>Note:</strong> Your processed file will be available for download for 7 days.</p>
        
        <br>
        <p>Thank you for using MetaFold!</p>
        <p>Best regards,<br>MetaFold Team</p>
        
        <hr>
        <small>If you have any questions, please contact our support team.</small>
    </body>
    </html>
    """
    
    try:
        # Send email with attachment
        send_email(job.user_email, subject, body, output_path)
    except Exception as e:
        logger.error(f"Failed to send completion email for job {job_id}: {e}")

def send_failure_email(job_id: str, error_message: str):
    """Send email notification when processing fails"""
    job = jobs[job_id]
    
    subject = f"MetaFold Processing Failed - {job.filename}"
    body = f"""
    <html>
    <body>
        <h2>MetaFold Processing Failed</h2>
        <p>Hello,</p>
        <p>We're sorry to inform you that the processing of your file has failed.</p>
        
        <h3>Job Details:</h3>
        <ul>
            <li><strong>Job ID:</strong> {job.id}</li>
            <li><strong>File:</strong> {job.filename}</li>
            <li><strong>Uploaded:</strong> {job.uploaded_at}</li>
            <li><strong>Error:</strong> {error_message}</li>
        </ul>
        
        <p>Please check your file format and try again. If the problem persists, please contact our support team with the Job ID.</p>
        
        <br>
        <p>Best regards,<br>MetaFold Team</p>
        
        <hr>
        <small>For support, please include the Job ID: {job_id}</small>
    </body>
    </html>
    """
    
    try:
        send_email(job.user_email, subject, body)
    except Exception as e:
        logger.error(f"Failed to send failure email for job {job_id}: {e}")

def update_job_status(job_id: str, processed_rows: int):
    """Callback to update job processing status"""
    if job_id in jobs:
        jobs[job_id].processed_rows = processed_rows

@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    progress_percent = 0
    if job.total_rows > 0:
        if job.status == "completed":
            progress_percent = 100
        else:
            progress_percent = int((job.processed_rows / job.total_rows) * 100)
    
    return {
        "id": job.id,
        "status": job.status,
        "filename": job.filename,
        "user_email": job.user_email,
        "uploaded_at": job.uploaded_at,
        "completed_at": job.completed_at,
        "progress": f"{job.processed_rows}/{job.total_rows}" if job.total_rows > 0 else "0/0",
        "progress_percent": progress_percent,
        "error": job.error
    }

@app.get("/api/jobs")
async def list_jobs():
    return list(jobs.values())

@app.get("/api/visits")
async def get_visits():
    """Get current visit count"""
    try:
        visit_doc = visits_collection.find_one({"_id": "visits"})
        if visit_doc:
            return VisitResponse(count=visit_doc["count"])
        else:
            return VisitResponse(count=157)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/visits")
async def increment_visits():
    """Increment visit count and return new count"""
    try:
        # Increment the visit count atomically
        result = visits_collection.find_one_and_update(
            {"_id": "visits"},
            {"$inc": {"count": 1}},
            upsert=True,
            return_document=True
        )
        
        return VisitResponse(count=result["count"])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/download/{job_id}")
async def download_file(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed yet")
    
    output_path = os.path.join(PROCESSED_DIR, f"{job_id}_processed_{job.filename}")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Processed file not found")
    
    return FileResponse(
        path=output_path, 
        filename=f"processed_{job.filename}",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/api/preview/{job_id}")
async def preview_data(job_id: str, limit: int = 100):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed yet")
    
    output_path = os.path.join(PROCESSED_DIR, f"{job_id}_processed_{job.filename}")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Processed file not found")
    
    try:
        df = pd.read_excel(output_path)
        # Convert DataFrame to JSON compatible format
        result = df.head(limit).fillna("").to_dict(orient="records")
        columns = df.columns.tolist()
        
        return {
            "columns": columns,
            "data": result,
            "total_rows": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Render!"}