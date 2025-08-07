"""
Complete Backend API for ResumeGPT with Conversation Memory
Provides clean REST endpoints for frontend applications
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys
import logging

# Add services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.resume_service import ResumeProcessor
from services.vector_service import VectorService
from services.conversation_service import ConversationService
from services.generation_service import gen_cover_letter, gen_interview_questions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="ResumeGPT API",
    description="Backend API for ResumeGPT with conversation memory",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, use proper state management)
conversation_service: Optional[ConversationService] = None

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    question: str
    memory_type: str = "buffer"

class ClearMemoryRequest(BaseModel):
    confirm: bool = True

class CoverLetterRequest(BaseModel):
    job_description: str

class InterviewRequest(BaseModel):
    role: str

class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    error: str
    details: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ResumeGPT API is running"}

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "ResumeGPT API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /upload - Upload and process resume",
            "ask": "POST /ask - Ask questions with memory",
            "clear-memory": "POST /clear-memory - Clear conversation memory",
            "memory-summary": "GET /memory-summary - Get memory usage",
            "cover-letter": "GET /cover-letter - Generate cover letter",
            "interview": "GET /interview - Generate interview questions"
        }
    }

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and process resume file"""
    global conversation_service
    
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT files."
            )
        
        # Create uploads directory
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Saved uploaded file: {file_path}")
        
        # Process resume
        processor = ResumeProcessor()
        chunks = processor.load_resume(file_path)
        
        logger.info(f"Processed resume into {len(chunks)} chunks")
        
        # Create vector store
        vector_service = VectorService()
        vector_store = vector_service.create_vector_store(chunks)
        
        # Initialize conversation service
        conversation_service = ConversationService(vector_store, memory_type="buffer")
        
        logger.info("Conversation service initialized")
        
        return {
            "status": "success",
            "message": f"Resume '{file.filename}' processed successfully",
            "data": {
                "filename": file.filename,
                "chunks_created": len(chunks),
                "file_size": len(content)
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question with conversation memory"""
    global conversation_service
    
    if not conversation_service:
        raise HTTPException(
            status_code=400,
            detail="No resume uploaded. Please upload a resume first."
        )
    
    try:
        # Switch memory type if different
        if conversation_service.memory_type != request.memory_type:
            conversation_service.switch_memory_type(request.memory_type)
            logger.info(f"Switched to {request.memory_type} memory")
        
        # Get response
        response = conversation_service.ask_question(request.question)
        
        return {
            "status": "success",
            "question": response["question"],
            "answer": response["answer"],
            "sources": response["source_chunks"],
            "conversation_length": len(response["chat_history"])
        }
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

@app.post("/clear-memory")
async def clear_conversation_memory(request: ClearMemoryRequest):
    """Clear conversation history"""
    global conversation_service
    
    if not conversation_service:
        raise HTTPException(
            status_code=400,
            detail="No conversation service initialized"
        )
    
    if not request.confirm:
        return {
            "status": "cancelled",
            "message": "Memory clear cancelled"
        }
    
    try:
        conversation_service.clear_memory()
        logger.info("Conversation memory cleared")
        
        return {
            "status": "success",
            "message": "Conversation memory cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Error clearing memory: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing memory: {str(e)}"
        )

@app.get("/memory-summary")
async def get_memory_summary():
    """Get conversation memory summary"""
    global conversation_service
    
    if not conversation_service:
        raise HTTPException(
            status_code=400,
            detail="No conversation service initialized"
        )
    
    try:
        summary = conversation_service.get_memory_summary()
        
        return {
            "status": "success",
            "memory_summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error getting memory summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting memory summary: {str(e)}"
        )

@app.get("/cover-letter")
async def generate_cover_letter(job_desc: str):
    """Generate cover letter based on resume and job description"""
    if not job_desc.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required"
        )
    
    try:
        cover_letter = gen_cover_letter(job_desc)
        
        return {
            "status": "success",
            "cover_letter": cover_letter
        }
        
    except Exception as e:
        logger.error(f"Error generating cover letter: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating cover letter: {str(e)}"
        )

@app.get("/interview")
async def generate_interview_questions(role: str):
    """Generate interview questions for specific role"""
    if not role.strip():
        raise HTTPException(
            status_code=400,
            detail="Role is required"
        )
    
    try:
        questions = gen_interview_questions(role)
        
        return {
            "status": "success",
            "questions": questions
        }
        
    except Exception as e:
        logger.error(f"Error generating interview questions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating interview questions: {str(e)}"
        )

# Alternative POST endpoints for complex requests
@app.post("/cover-letter")
async def generate_cover_letter_post(request: CoverLetterRequest):
    """Generate cover letter (POST version)"""
    return await generate_cover_letter(request.job_description)

@app.post("/interview")
async def generate_interview_questions_post(request: InterviewRequest):
    """Generate interview questions (POST version)"""
    return await generate_interview_questions(request.role)

# Debug endpoints (remove in production)
@app.get("/debug/conversation-state")
async def debug_conversation_state():
    """Debug endpoint to see conversation state"""
    global conversation_service
    
    if not conversation_service:
        return {"error": "No conversation service"}
    
    try:
        conversation_service.debug_memory()
        summary = conversation_service.get_memory_summary()
        
        return {
            "status": "success",
            "debug_info": {
                "memory_summary": summary,
                "service_initialized": True,
                "memory_type": conversation_service.memory_type
            }
        }
        
    except Exception as e:
        return {"error": f"Debug error: {str(e)}"}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "status": "error",
        "error": "Endpoint not found",
        "available_endpoints": [
            "/health", "/upload", "/ask", "/clear-memory", 
            "/memory-summary", "/cover-letter", "/interview"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "status": "error",
        "error": "Internal server error",
        "message": "Something went wrong. Please check the logs."
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting ResumeGPT Backend API...")
    print("📋 Available endpoints:")
    print("   - http://localhost:8000/health")
    print("   - http://localhost:8000/docs (API documentation)")
    print("   - http://localhost:8000/upload")
    print("   - http://localhost:8000/ask")
    print("")
    print("💡 Start the frontend with: streamlit run frontend/streamlit/chat_app.py")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
