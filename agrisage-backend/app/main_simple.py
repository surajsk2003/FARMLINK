from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

# Initialize FastAPI
app = FastAPI(
    title="FarmLink API",
    description="Agricultural Intelligence Assistant API - 100% FREE",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QuestionRequest(BaseModel):
    question: str
    language: str = "en"

class AgriResponse(BaseModel):
    response: str
    confidence: float
    model_used: str
    source: str
    success: bool
    processing_time: float = 0.0
    cost: str = "FREE"

# Simple knowledge base
SIMPLE_ANSWERS = {
    "wheat": "For wheat crop: Apply NPK in ratio 120:60:40 kg/hectare. Use DAP at sowing. Apply urea in 2-3 splits. Best sowing time: November 15 - December 15 in North India.",
    "rice": "Rice requires 1200-1500mm annual rainfall. Transplant 25-30 day old seedlings. Apply 150:75:75 kg NPK/hectare. Harvest when 80-85% grains turn golden yellow.",
    "cotton": "Use Bt cotton varieties for bollworm resistance. Install pheromone traps 5-10/hectare. Apply balanced NPK fertilizers. Control whitefly to prevent leaf curl virus.",
    "fertilizer": "Apply balanced NPK fertilizers based on soil test. Use organic manure like FYM 10-15 tons/hectare. For organic farming, use vermicompost 5-8 tons/hectare.",
    "pest": "Use Integrated Pest Management (IPM). Install pheromone traps. Use neem-based organic pesticides. Maintain field hygiene. Crop rotation helps break pest cycles.",
    "crop": "Complete guide to crop cultivation: 1) Soil preparation with proper pH 2) Quality seed selection 3) Timely sowing 4) Balanced nutrition 5) Water management 6) Pest control 7) Proper harvesting",
    "pm-kisan": "PM-KISAN provides ₹6000 per year to farmer families in 3 installments of ₹2000 each. Direct cash transfer to bank account. No land size restriction. Apply through pmkisan.gov.in"
}

@app.get("/")
async def root():
    return {
        "message": "FarmLink API is running! 🌾",
        "version": "2.0.0",
        "cost": "100% FREE",
        "docs": "/docs",
        "features": [
            "Multi-language support (English/Hindi)",
            "SMS integration", 
            "Agricultural knowledge base",
            "Government schemes info"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "uptime": "running",
        "services": {
            "knowledge_base": "active",
            "sms_service": "active"
        }
    }

@app.post("/ask", response_model=AgriResponse)
async def ask_question(request: QuestionRequest):
    try:
        import time
        start_time = time.time()
        
        question = request.question.lower()
        
        # Simple keyword-based matching
        response = "I'm a simple agricultural assistant. For detailed guidance, consult local agricultural extension services or Krishi Vigyan Kendra."
        
        for keyword, answer in SIMPLE_ANSWERS.items():
            if keyword in question:
                response = answer
                break
        
        processing_time = time.time() - start_time
        
        return AgriResponse(
            response=response,
            confidence=0.8,
            model_used="Simple Knowledge Base",
            source="Agricultural Guidelines",
            success=True,
            processing_time=processing_time,
            cost="FREE"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/categories")
async def get_categories():
    return {
        "categories": [
            "fertilization", "pest_control", "crop_health", 
            "water_management", "government_schemes"
        ]
    }

@app.get("/free-services")
async def get_free_services():
    return {
        "sms_providers": {
            "demo": {"limit": "Unlimited", "region": "Global", "cost": "FREE"}
        },
        "ai_providers": {
            "simple_kb": {"models": ["Basic Agricultural Knowledge"], "cost": "FREE"}
        }
    }

# Include simple SMS endpoint
@app.post("/sms/send")
async def send_sms_demo():
    return {
        "success": True,
        "message": "SMS sent successfully",
        "details": {
            "provider": "demo_mode",
            "cost": "FREE",
            "note": "Demo mode - SMS simulation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))