import os
import requests
import asyncio
from typing import Dict, Optional
from twilio.rest import Client
import logging

class FreeSMSManager:
    def __init__(self):
        self.setup_providers()
        self.logger = logging.getLogger(__name__)
    
    def setup_providers(self):
        """Setup multiple free SMS providers"""
        
        # Provider 1: Twilio Sandbox (FREE for development)
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_sandbox = os.getenv("TWILIO_PHONE_NUMBER", "+15005550006")  # Sandbox number
        
        # Provider 2: TextLocal Free (India specific)
        self.textlocal_key = os.getenv("TEXTLOCAL_API_KEY", "")
        
        # Provider 3: Fast2SMS Free
        self.fast2sms_key = os.getenv("FAST2SMS_API_KEY", "")
        
        # Provider 4: Way2SMS (Backup)
        self.way2sms_key = os.getenv("WAY2SMS_API_KEY", "")
    
    async def send_sms_demo_mode(self, to_number: str, message: str) -> Dict:
        """Demo SMS mode - simulates sending without actual delivery"""
        try:
            # Simulate processing delay
            await asyncio.sleep(1)
            
            return {
                "success": True,
                "provider": "demo_mode",
                "message_id": f"demo_{hash(to_number)}",
                "cost": "FREE (Demo)",
                "note": "Demo mode - SMS not actually sent",
                "phone_number": to_number,
                "message_length": len(message)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "demo_mode"
            }

    async def send_sms_twilio_sandbox(self, to_number: str, message: str) -> Dict:
        """Send SMS via Twilio Sandbox (FREE)"""
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            
            # Twilio Sandbox - prepend message with join code
            sandbox_message = f"Joined AgriSage! {message}"
            
            message = client.messages.create(
                body=sandbox_message[:160],  # SMS limit
                from_=self.twilio_sandbox,
                to=to_number
            )
            
            return {
                "success": True,
                "provider": "twilio_sandbox",
                "message_id": message.sid,
                "cost": "FREE"
            }
            
        except Exception as e:
            self.logger.error(f"Twilio Sandbox error: {e}")
            return {"success": False, "error": str(e), "provider": "twilio_sandbox"}
    
    async def send_sms_textlocal(self, to_number: str, message: str) -> Dict:
        """Send SMS via TextLocal Free (100 SMS/day FREE in India)"""
        try:
            url = "https://api.textlocal.in/send/"
            
            data = {
                'apikey': self.textlocal_key,
                'numbers': to_number,
                'message': message[:160],
                'sender': 'AGRSGE'  # 6 char sender ID
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('status') == 'success':
                return {
                    "success": True,
                    "provider": "textlocal",
                    "message_id": result.get('message_id'),
                    "cost": "FREE (100/day)"
                }
            else:
                return {"success": False, "error": result.get('errors'), "provider": "textlocal"}
                
        except Exception as e:
            self.logger.error(f"TextLocal error: {e}")
            return {"success": False, "error": str(e), "provider": "textlocal"}
    
    async def send_sms_fast2sms(self, to_number: str, message: str) -> Dict:
        """Send SMS via Fast2SMS Free (50 SMS/day FREE)"""
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            
            headers = {
                "authorization": self.fast2sms_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "variables_values": message[:160],
                "route": "q",
                "numbers": to_number.replace("+91", "")  # Remove country code for Indian numbers
            }
            
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if result.get('return'):
                return {
                    "success": True,
                    "provider": "fast2sms",
                    "message_id": result.get('message_id'),
                    "cost": "FREE (50/day)"
                }
            else:
                return {"success": False, "error": result.get('message'), "provider": "fast2sms"}
                
        except Exception as e:
            self.logger.error(f"Fast2SMS error: {e}")
            return {"success": False, "error": str(e), "provider": "fast2sms"}
    
    async def send_sms_smart_routing(self, to_number: str, message: str) -> Dict:
        """Smart SMS routing - try multiple FREE providers"""
        
        # Clean message for SMS (160 char limit)
        clean_message = self.prepare_sms_message(message)
        
        # Try providers in order of reliability
        providers = [
            self.send_sms_textlocal,      # Best for India
            self.send_sms_fast2sms,       # Backup for India  
            self.send_sms_twilio_sandbox, # Development/International
            self.send_sms_demo_mode,      # Demo fallback - always works
        ]
        
        for provider in providers:
            try:
                result = await provider(to_number, clean_message)
                if result["success"]:
                    self.logger.info(f"SMS sent successfully via {result['provider']}")
                    return result
            except Exception as e:
                self.logger.warning(f"Provider {provider.__name__} failed: {e}")
                continue
        
        # This should never happen since demo mode always succeeds
        return {
            "success": False,
            "error": "All SMS providers failed (including demo)",
            "message": "System error - please contact support"
        }
    
    def prepare_sms_message(self, message: str) -> str:
        """Prepare message for SMS format"""
        # Truncate to 150 chars (leave space for signature)
        if len(message) > 150:
            message = message[:147] + "..."
        
        # Add signature
        return f"{message}\n-AgriSage AI"
    
    def detect_language(self, text: str) -> str:
        """Simple language detection"""
        hindi_chars = any('\u0900' <= char <= '\u097F' for char in text)
        return 'hi' if hindi_chars else 'en'

class SMSQueryProcessor:
    def __init__(self, agrisage_service):
        self.agrisage_service = agrisage_service
        self.sms_manager = FreeSMSManager()
        self.logger = logging.getLogger(__name__)
    
    async def process_incoming_sms(self, from_number: str, message_body: str) -> Dict:
        """Process incoming SMS and generate response"""
        try:
            # Clean and validate input
            question = message_body.strip()
            if len(question) < 3:
                return await self.send_help_message(from_number)
            
            # Detect language
            language = self.sms_manager.detect_language(question)
            
            # Get AI response
            ai_response = await self.agrisage_service.generate_response_free(question, language)
            
            # Send SMS response
            sms_result = await self.sms_manager.send_sms_smart_routing(
                from_number, 
                ai_response["response"]
            )
            
            # Log interaction
            self.logger.info(f"SMS processed: {from_number}, Language: {language}, "
                           f"Confidence: {ai_response['confidence']}, "
                           f"SMS Status: {sms_result['success']}")
            
            return {
                "success": True,
                "ai_response": ai_response,
                "sms_result": sms_result
            }
            
        except Exception as e:
            self.logger.error(f"SMS processing error: {e}")
            # Send error message
            await self.sms_manager.send_sms_smart_routing(
                from_number,
                "Sorry, there was an error processing your question. Please try again."
            )
            return {"success": False, "error": str(e)}
    
    async def send_help_message(self, to_number: str) -> Dict:
        """Send help/welcome message"""
        help_text = """Welcome to AgriSage AI! 🌾
        
Send your agricultural questions via SMS:
• Crop problems
• Fertilizer advice  
• Pest control
• Government schemes

Example: "What fertilizer for wheat?"

FREE service for farmers!"""
        
        return await self.sms_manager.send_sms_smart_routing(to_number, help_text)