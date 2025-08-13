from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from app.services.knowledge_base import AgricultureKnowledgeBase
from app.services.free_ai_clients import FreeAIOrchestrator
from app.routers import sms

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="AgriSage AI API",
    description="Agricultural Intelligence Assistant API - 100% FREE",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instances
knowledge_base = None
agrisage_service = None

@app.on_event("startup")
async def startup_event():
    global knowledge_base, agrisage_service
    print("🌾 Initializing AgriSage AI API...")
    
    # Initialize knowledge base
    knowledge_base = AgricultureKnowledgeBase()
    
    # Initialize AI orchestrator
    agrisage_service = FreeAIOrchestrator(knowledge_base)
    
    print("✅ AgriSage AI API ready!")

# Request/Response Models
class QuestionRequest(BaseModel):
    question: str
    language: str = "en"
    context: str = ""

class AgriResponse(BaseModel):
    response: str
    confidence: float
    model_used: str
    source: str
    success: bool
    processing_time: float = 0.0
    cost: str = "FREE"

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: str
    services: dict
    cost_info: dict

# Include routers
app.include_router(sms.router)

# Routes
@app.get("/")
async def root():
    return {
        "message": "AgriSage AI API is running! 🌾",
        "version": "2.0.0",
        "cost": "100% FREE",
        "docs": "/docs",
        "features": [
            "Multi-language support (English/Hindi)",
            "SMS integration", 
            "Free AI models",
            "Agricultural knowledge base",
            "Government schemes info"
        ]
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        uptime="running",
        services={
            "knowledge_base": "active",
            "ai_orchestrator": "active",
            "sms_service": "active",
            "groq_client": "configured",
            "huggingface_client": "configured",
            "ollama_client": "optional"
        },
        cost_info={
            "api_usage": "FREE",
            "sms_limits": {
                "textlocal": "100 SMS/day",
                "fast2sms": "50 SMS/day",
                "twilio_sandbox": "unlimited (dev only)"
            },
            "ai_limits": {
                "groq": "generous free tier",
                "huggingface": "1000 requests/month",
                "knowledge_base": "unlimited (local)"
            }
        }
    )

@app.post("/ask", response_model=AgriResponse)
async def ask_question(request: QuestionRequest):
    try:
        import time
        start_time = time.time()
        
        if not agrisage_service:
            raise HTTPException(status_code=503, detail="AgriSage AI not initialized")
        
        # Generate response using FREE services
        result = await agrisage_service.generate_response_free(
            question=request.question,
            language=request.language
        )
        
        processing_time = time.time() - start_time
        
        return AgriResponse(
            response=result["response"],
            confidence=result["confidence"],
            model_used=result["model_used"],
            source=result["source"],
            success=result["success"],
            processing_time=processing_time,
            cost=result.get("cost", "FREE")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get available agricultural categories"""
    return {
        "categories": [
            "fertilization",
            "pest_control",
            "disease_control", 
            "crop_health",
            "water_management",
            "harvesting",
            "government_schemes",
            "organic_farming",
            "crop_calendar"
        ]
    }

@app.get("/crops")
async def get_supported_crops():
    """Get list of supported crops"""
    return {
        "crops": [
            "wheat", "rice", "cotton", "tomato", "maize", 
            "sugarcane", "potato", "onion", "vegetables", "general"
        ]
    }

@app.get("/free-services")
async def get_free_services():
    """Information about all FREE services available"""
    return {
        "sms_providers": {
            "textlocal": {
                "limit": "100 SMS/day",
                "region": "India",
                "cost": "FREE"
            },
            "fast2sms": {
                "limit": "50 SMS/day", 
                "region": "India",
                "cost": "FREE"
            },
            "twilio_sandbox": {
                "limit": "Unlimited",
                "region": "Global",
                "cost": "FREE (Development only)"
            }
        },
        "ai_providers": {
            "groq": {
                "models": ["llama3-8b-8192"],
                "speed": "Ultra-fast",
                "cost": "FREE"
            },
            "huggingface": {
                "models": ["Multiple open-source models"],
                "limit": "1000 requests/month",
                "cost": "FREE"
            },
            "ollama": {
                "models": ["Local models"],
                "limit": "Unlimited",
                "cost": "FREE (Local)"
            },
            "knowledge_base": {
                "type": "Agricultural expert knowledge",
                "limit": "Unlimited",
                "cost": "FREE"
            }
        },
        "translation": {
            "google_translate": {
                "limit": "500K characters/month",
                "cost": "FREE"
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)