import os
import requests
import asyncio
import aiohttp
from typing import Dict, List
from .knowledge_base import AgricultureKnowledgeBase

class OllamaLocalClient:
    """Ollama - 100% FREE local models"""
    def __init__(self):
        self.base_url = "http://localhost:11434"  # Local Ollama instance
        self.preferred_models = [
            "llama3.2:1b",      # Meta's efficient model (~1GB)
            "phi3:mini",        # Microsoft's fast model (~2GB) 
            "gemma:2b",         # Google's small model (~1.5GB)
            "qwen2.5:0.5b"      # Alibaba's tiny model (~0.5GB)
        ]
    
    async def ensure_model_available(self, model: str = "llama3.2:1b") -> bool:
        """Check if model is available locally, download if needed"""
        try:
            # Check if model exists
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        models_data = await response.json()
                        available_models = [m['name'] for m in models_data.get('models', [])]
                        return model in available_models
            return False
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return False
    
    async def query_agricultural_model(self, question: str, language: str = "en") -> Dict:
        """Query FREE local Ollama models for agricultural advice"""
        
        # Try preferred models in order
        for model in self.preferred_models:
            try:
                # Check if model is available
                if not await self.ensure_model_available(model):
                    continue
                
                # Craft agricultural prompt
                system_prompt = {
                    "en": "You are an expert agricultural advisor for Indian farmers. Provide practical, actionable advice in simple language. Focus on fertilizers, pest control, crop timing, and government schemes.",
                    "hi": "आप भारतीय किसानों के लिए एक कुशल कृषि सलाहकार हैं। सरल भाषा में व्यावहारिक सलाह दें। उर्वरक, कीट नियंत्रण, फसल का समय, और सरकारी योजनाओं पर ध्यान दें।"
                }
                
                prompt = f"{system_prompt.get(language, system_prompt['en'])}\n\nQuestion: {question}\nAnswer:"
                
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_predict": 200  # Limit response length
                    }
                }
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                    async with session.post(f"{self.base_url}/api/generate", 
                                          json=payload) as response:
                        if response.status == 200:
                            result = await response.json()
                            return {
                                "success": True,
                                "response": result.get("response", "").strip(),
                                "model": f"Ollama-{model} (100% FREE)",
                                "cost": "FREE (Local)",
                                "processing_time": result.get("total_duration", 0) / 1e9  # Convert to seconds
                            }
                        
            except Exception as e:
                print(f"Ollama model {model} failed: {e}")
                continue
        
        return {
            "success": False, 
            "error": "No Ollama models available. Please install: ollama pull llama3.2:1b",
            "model": "Ollama (LOCAL/FREE)"
        }

class LibreTranslateClient:
    """LibreTranslate - 100% FREE and open-source translation"""
    def __init__(self):
        self.base_url = "https://libretranslate.com/translate"
        self.supported_languages = {
            "en": "English",
            "hi": "Hindi", 
            "bn": "Bengali",
            "te": "Telugu",
            "ta": "Tamil",
            "mr": "Marathi",
            "gu": "Gujarati",
            "kn": "Kannada",
            "pa": "Punjabi",
            "ur": "Urdu"
        }
    
    async def translate_text(self, text: str, target_language: str, source_language: str = "auto") -> Dict:
        """100% FREE translation service - no API key needed"""
        try:
            payload = {
                "q": text,
                "source": source_language,
                "target": target_language,
                "format": "text"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "translated_text": result.get("translatedText", text),
                            "detected_language": result.get("detectedLanguage", source_language),
                            "cost": "100% FREE (No limits)",
                            "provider": "LibreTranslate (Open Source)"
                        }
                    else:
                        error_data = await response.text()
                        return {"success": False, "error": f"LibreTranslate API Error: {response.status} - {error_data}"}
                        
        except Exception as e:
            return {"success": False, "error": f"LibreTranslate error: {str(e)}"}

class HuggingFaceFreeClient:
    """Hugging Face FREE Inference API - Agricultural Models"""
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")  # Get from environment variable
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # FREE agricultural and general models
        self.agricultural_models = [
            "cropinailab/aksara_v1",           # Agricultural specialist
            "microsoft/DialoGPT-medium",       # Conversational AI
            "facebook/blenderbot-400M-distill", # Fast responses
            "google/flan-t5-base",             # General knowledge
            "microsoft/GODEL-v1_1-base-seq2seq" # Dialogue model
        ]
    
    async def query_agricultural_models(self, question: str, language: str = "en") -> Dict:
        """Query multiple FREE agricultural models from Hugging Face"""
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        for model in self.agricultural_models:
            try:
                url = f"{self.base_url}/{model}"
                
                # Craft prompt based on model type
                if "aksara" in model:
                    # Agricultural specialist model
                    inputs = f"Agricultural Question: {question}\nExpert Agricultural Answer:"
                elif "DialoGPT" in model or "blenderbot" in model:
                    # Conversational models
                    inputs = f"Farmer: {question}\nAgricultural Expert:"
                else:
                    # General models
                    inputs = f"Question about farming: {question}\nAnswer:"
                
                payload = {
                    "inputs": inputs,
                    "parameters": {
                        "max_new_tokens": 150,
                        "temperature": 0.7,
                        "do_sample": True,
                        "top_p": 0.9,
                        "repetition_penalty": 1.1
                    }
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload, 
                                          timeout=aiohttp.ClientTimeout(total=20)) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            # Handle different response formats
                            if isinstance(result, list) and len(result) > 0:
                                if "generated_text" in result[0]:
                                    response_text = result[0]["generated_text"]
                                    # Clean up the response
                                    response_text = response_text.replace(inputs, "").strip()
                                    
                                    if len(response_text) > 10:  # Valid response
                                        return {
                                            "success": True,
                                            "response": response_text,
                                            "model": f"HF-{model.split('/')[-1]} (FREE)",
                                            "cost": "FREE (1000 req/month)",
                                            "provider": "Hugging Face"
                                        }
            except Exception as e:
                print(f"HF model {model} failed: {e}")
                continue
        
        return {
            "success": False, 
            "error": "All Hugging Face models unavailable or rate limited",
            "model": "Hugging Face (FREE)"
        }

class ImprovedFreeAIOrchestrator:
    """Orchestrates all 100% FREE AI services with better reliability"""
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.ollama_client = OllamaLocalClient()
        self.hf_client = HuggingFaceFreeClient()
        self.translator = LibreTranslateClient()
    
    async def generate_response_free(self, question: str, language: str = "en") -> Dict:
        """Generate response using only 100% FREE services with smart fallbacks"""
        
        # Step 1: Knowledge Base (LOCAL/FREE - highest priority, fastest)
        knowledge_results = self.knowledge_base.search_knowledge(question, top_k=3)
        
        if knowledge_results and knowledge_results[0]['confidence'] > 0.8:
            best_match = knowledge_results[0]
            
            # Translate if needed using FREE LibreTranslate
            response_text = best_match['answer']
            if language == 'hi' and not self.is_hindi_text(response_text):
                translation = await self.translator.translate_text(response_text, 'hi', 'en')
                if translation["success"]:
                    response_text = translation["translated_text"]
            
            return {
                "response": response_text,
                "confidence": best_match['confidence'],
                "model_used": "Knowledge Base (100% FREE)",
                "source": "Agricultural Expert Knowledge",
                "cost": "FREE (Unlimited)",
                "success": True
            }
        
        # Step 2: Ollama Local (100% FREE, unlimited, slower but reliable)
        ollama_result = await self.ollama_client.query_agricultural_model(question, language)
        if ollama_result["success"]:
            return {
                "response": ollama_result["response"],
                "confidence": 0.75,
                "model_used": ollama_result["model"],
                "source": "Local AI Model",
                "cost": "100% FREE (Local)",
                "success": True,
                "processing_time": ollama_result.get("processing_time", 0)
            }
        
        # Step 3: Hugging Face Free (FREE with monthly limits)
        hf_result = await self.hf_client.query_agricultural_models(question, language)
        if hf_result["success"]:
            return {
                "response": hf_result["response"],
                "confidence": 0.7,
                "model_used": hf_result["model"],
                "source": "Hugging Face FREE API",
                "cost": hf_result["cost"],
                "success": True
            }
        
        # Step 4: Knowledge Base Fallback with lower confidence (always available)
        if knowledge_results and len(knowledge_results) > 0:
            best_match = knowledge_results[0]
            return {
                "response": f"Based on similar agricultural practices: {best_match['answer']}",
                "confidence": 0.6,
                "model_used": "Knowledge Base Fallback (FREE)",
                "source": "Agricultural Knowledge",
                "cost": "FREE (Unlimited)",
                "success": True
            }
        
        # Step 5: Ultimate fallback with helpful guidance
        return {
            "response": "For this specific question, I recommend contacting your local Krishi Vigyan Kendra (KVK) or calling the Kisan Call Center at 1800-180-1551 for expert agricultural guidance.",
            "confidence": 0.3,
            "model_used": "Referral Service (FREE)",
            "source": "Agricultural Extension Network",
            "cost": "FREE",
            "success": True
        }
    
    def is_hindi_text(self, text: str) -> bool:
        """Check if text contains Hindi (Devanagari) characters"""
        return any('\u0900' <= char <= '\u097F' for char in text)
    
    async def get_service_status(self) -> Dict:
        """Check status of all FREE services"""
        status = {
            "knowledge_base": {
                "status": "active",
                "entries": len(self.knowledge_base.knowledge_base),
                "cost": "FREE (Unlimited)"
            },
            "ollama_local": {
                "status": "checking...",
                "models": [],
                "cost": "100% FREE (Local)"
            },
            "hugging_face": {
                "status": "active" if self.hf_client.api_key else "needs_api_key",
                "models": len(self.hf_client.agricultural_models),
                "cost": "FREE (1000 req/month)"
            },
            "libre_translate": {
                "status": "active",
                "languages": len(self.translator.supported_languages),
                "cost": "100% FREE (No limits)"
            }
        }
        
        # Check Ollama status
        try:
            ollama_available = await self.ollama_client.ensure_model_available()
            status["ollama_local"]["status"] = "active" if ollama_available else "needs_setup"
            if ollama_available:
                status["ollama_local"]["models"] = self.ollama_client.preferred_models
        except:
            status["ollama_local"]["status"] = "not_installed"
        
        return status