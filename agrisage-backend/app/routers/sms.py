from fastapi import APIRouter, Request, Form, HTTPException
from app.services.sms_service import SMSQueryProcessor, FreeSMSManager
from app.services.knowledge_base import AgricultureKnowledgeBase
from app.services.free_ai_clients import FreeAIOrchestrator
import logging

router = APIRouter(prefix="/sms", tags=["SMS"])
logger = logging.getLogger(__name__)

# Initialize services
knowledge_base = AgricultureKnowledgeBase()
agrisage_service = FreeAIOrchestrator(knowledge_base)
sms_processor = SMSQueryProcessor(agrisage_service)

@router.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    """Handle incoming SMS from Twilio Sandbox"""
    try:
        form_data = await request.form()
        from_number = form_data.get("From", "")
        message_body = form_data.get("Body", "")
        
        logger.info(f"Twilio SMS received from {from_number}: {message_body}")
        
        # Process SMS
        result = await sms_processor.process_incoming_sms(from_number, message_body)
        
        # Twilio expects TwiML response
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>Processing your agricultural question...</Message>
        </Response>"""
        
    except Exception as e:
        logger.error(f"Twilio webhook error: {e}")
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Message>Error processing your message. Please try again.</Message>
        </Response>"""

@router.post("/webhook/textlocal")
async def textlocal_webhook(request: Request):
    """Handle incoming SMS from TextLocal"""
    try:
        form_data = await request.form()
        from_number = form_data.get("inNumber", "")
        message_body = form_data.get("content", "")
        
        logger.info(f"TextLocal SMS received from {from_number}: {message_body}")
        
        # Process SMS
        result = await sms_processor.process_incoming_sms(from_number, message_body)
        
        return {"status": "success", "message": "SMS processed"}
        
    except Exception as e:
        logger.error(f"TextLocal webhook error: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/send")
async def send_sms_manual(request: Request):
    """Manual SMS sending endpoint for testing"""
    try:
        # Handle both query params and form data
        form_data = await request.form()
        query_params = request.query_params
        
        phone_number = (
            query_params.get("phone_number") or 
            form_data.get("phone_number") or
            query_params.get("phoneNumber") or
            form_data.get("phoneNumber")
        )
        message = (
            query_params.get("message") or 
            form_data.get("message")
        )
        
        if not phone_number or not message:
            raise HTTPException(status_code=400, detail="Phone number and message are required")
        
        logger.info(f"Manual SMS request: {phone_number} -> {message[:50]}...")
        
        sms_manager = FreeSMSManager()
        result = await sms_manager.send_sms_smart_routing(
            phone_number, message
        )
        
        return {
            "success": True,
            "message": "SMS sent successfully",
            "details": result,
            "phone_number": phone_number
        }
        
    except Exception as e:
        logger.error(f"Manual SMS error: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to send SMS"
        }

@router.get("/test")
async def test_sms_service():
    """Test SMS service status"""
    return {
        "status": "SMS service active",
        "providers": ["TextLocal (FREE 100/day)", "Fast2SMS (FREE 50/day)", "Twilio Sandbox (FREE dev)"],
        "features": ["Multi-language", "Smart routing", "Free tier"],
        "webhook_endpoints": {
            "twilio": "/sms/webhook/twilio",
            "textlocal": "/sms/webhook/textlocal"
        }
    }

@router.get("/providers")
async def get_sms_providers():
    """Get information about SMS providers"""
    return {
        "free_providers": {
            "textlocal": {
                "name": "TextLocal India",
                "free_limit": "100 SMS/day",
                "signup_url": "https://textlocal.in",
                "regions": ["India"],
                "webhook_support": True
            },
            "fast2sms": {
                "name": "Fast2SMS",
                "free_limit": "50 SMS/day",
                "signup_url": "https://fast2sms.com", 
                "regions": ["India"],
                "webhook_support": False
            },
            "twilio_sandbox": {
                "name": "Twilio Sandbox",
                "free_limit": "Unlimited (Dev only)",
                "signup_url": "https://twilio.com",
                "regions": ["Global"],
                "webhook_support": True,
                "note": "Development/testing only"
            }
        },
        "setup_instructions": {
            "textlocal": "1. Sign up at textlocal.in 2. Get API key 3. Set TEXTLOCAL_API_KEY env var",
            "fast2sms": "1. Sign up at fast2sms.com 2. Get API key 3. Set FAST2SMS_API_KEY env var",
            "twilio": "1. Sign up at twilio.com 2. Get SID/Token 3. Set TWILIO_* env vars"
        }
    }