from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv
from app.services.knowledge_base import AgricultureKnowledgeBase
from app.services.improved_free_ai_clients import ImprovedFreeAIOrchestrator
from app.routers import sms

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="KrishiConnect AI API",
    description="100% FREE Agricultural Intelligence Assistant API",
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
krishiconnect_service = None

@app.on_event("startup")
async def startup_event():
    global knowledge_base, krishiconnect_service
    print("🌾 Initializing KrishiConnect AI API...")
    
    # Initialize knowledge base
    knowledge_base = AgricultureKnowledgeBase()
    
    # Initialize improved FREE AI orchestrator
    krishiconnect_service = ImprovedFreeAIOrchestrator(knowledge_base)
    
    print("✅ KrishiConnect AI API ready!")

# Request/Response Models
class QuestionRequest(BaseModel):
    question: str
    language: str = "en"
    context: str = ""

class KrishiResponse(BaseModel):
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

# Include routers
app.include_router(sms.router)

# Routes
@app.get("/")
async def root():
    return {
        "message": "KrishiConnect AI API is running! 🌾",
        "version": "2.0.0",
        "cost": "100% FREE Forever",
        "docs": "/docs",
        "features": [
            "100% FREE AI models (Ollama + HuggingFace)",
            "Multi-language support (English/Hindi)", 
            "SMS integration (150+ FREE SMS/day)",
            "LibreTranslate (unlimited FREE translation)",
            "Agricultural knowledge base",
            "Government schemes information",
            "Voice input support",
            "Offline-capable with Ollama"
        ],
        "setup_required": [
            "1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh",
            "2. Download model: ollama pull llama3.2:1b",
            "3. Get HF token: YOUR_HUGGINGFACE_TOKEN",
            "4. Configure SMS providers (optional)",
            "5. Deploy and enjoy 100% FREE service!"
        ]
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    service_status = await krishiconnect_service.get_service_status() if krishiconnect_service else {}
    
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        uptime="running",
        services=service_status
    )

@app.post("/ask", response_model=KrishiResponse)
async def ask_question(request: QuestionRequest):
    try:
        import time
        start_time = time.time()
        
        if not krishiconnect_service:
            raise HTTPException(status_code=503, detail="KrishiConnect AI not initialized")
        
        # Generate response using 100% FREE services
        result = await krishiconnect_service.generate_response_free(
            question=request.question,
            language=request.language
        )
        
        processing_time = time.time() - start_time
        
        return KrishiResponse(
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
            "crop_calendar",
            "seed_varieties",
            "soil_management",
            "weather_advisory"
        ]
    }

@app.get("/crops")
async def get_supported_crops():
    """Get list of supported crops"""
    return {
        "crops": [
            "wheat", "rice", "cotton", "tomato", "maize", 
            "sugarcane", "potato", "onion", "vegetables", 
            "pulses", "mustard", "groundnut", "soybean",
            "millet", "barley", "chickpea", "general"
        ]
    }

@app.get("/free-stack")
async def get_free_stack():
    """Complete information about 100% FREE technology stack"""
    return {
        "ai_models": {
            "ollama": {
                "cost": "100% FREE Forever",
                "models": ["llama3.2:1b", "phi3:mini", "gemma:2b"],
                "setup": "curl -fsSL https://ollama.ai/install.sh | sh",
                "storage": "1-3 GB per model",
                "limits": "Unlimited (local processing)"
            },
            "hugging_face": {
                "cost": "FREE (1000 requests/month)",
                "models": ["cropinailab/aksara_v1", "microsoft/DialoGPT-medium"],
                "setup": "Get token from huggingface.co",
                "api_key": "YOUR_HF_TOKEN_HERE",
                "limits": "1000 API calls/month"
            }
        },
        "translation": {
            "libretranslate": {
                "cost": "100% FREE (No limits)",
                "api": "https://libretranslate.com/translate",
                "languages": ["English", "Hindi", "Bengali", "Tamil", "Telugu"],
                "setup": "No API key needed - works instantly!",
                "limits": "Unlimited (open source)"
            }
        },
        "sms_providers": {
            "textlocal": {
                "cost": "FREE (100 SMS/day)",
                "region": "India",
                "signup": "https://textlocal.in"
            },
            "fast2sms": {
                "cost": "FREE (50 SMS/day)",
                "region": "India", 
                "signup": "https://fast2sms.com"
            },
            "twilio_sandbox": {
                "cost": "FREE (Unlimited for dev)",
                "region": "Global",
                "signup": "https://twilio.com"
            }
        },
        "hosting": {
            "railway": {
                "cost": "FREE (500 hours/month)",
                "type": "Backend API hosting",
                "signup": "https://railway.app"
            },
            "vercel": {
                "cost": "FREE (Unlimited projects)",
                "type": "Frontend hosting", 
                "signup": "https://vercel.com"
            }
        },
        "total_monthly_cost": "₹0 (100% FREE!)",
        "scalability": "Handles millions of farmer questions",
        "languages_supported": "English + Hindi + 8 more",
        "offline_capability": "Yes (with Ollama)",
        "setup_time": "30 minutes"
    }

@app.get("/ollama-setup")
async def get_ollama_setup():
    """Step-by-step Ollama setup guide"""
    return {
        "title": "Ollama Setup - 100% FREE Local AI",
        "steps": [
            {
                "step": 1,
                "command": "curl -fsSL https://ollama.ai/install.sh | sh",
                "description": "Install Ollama (works on Linux, macOS, Windows)"
            },
            {
                "step": 2,
                "command": "ollama pull llama3.2:1b",
                "description": "Download agricultural AI model (~1GB)"
            },
            {
                "step": 3,
                "command": "ollama run llama3.2:1b 'What fertilizer for wheat?'",
                "description": "Test the model with agricultural question"
            },
            {
                "step": 4,
                "command": "ollama serve",
                "description": "Start Ollama server (runs on port 11434)"
            }
        ],
        "alternative_models": {
            "phi3:mini": "Microsoft's efficient model (~2GB)",
            "gemma:2b": "Google's optimized model (~1.5GB)", 
            "qwen2.5:0.5b": "Ultra-small model (~0.5GB)"
        },
        "benefits": [
            "100% FREE forever - no API costs",
            "Works offline - no internet needed after download",
            "Privacy-first - all data stays local",
            "Unlimited usage - no rate limits",
            "Fast responses - 2-5 seconds typical"
        ],
        "system_requirements": {
            "minimum": "4GB RAM, 2GB disk space",
            "recommended": "8GB RAM, 10GB disk space",
            "os": "Linux, macOS, Windows (WSL)"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)