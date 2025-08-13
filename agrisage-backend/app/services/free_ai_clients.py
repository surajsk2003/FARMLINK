import os
import requests
import asyncio
import aiohttp
from typing import Dict, List
from .knowledge_base import AgricultureKnowledgeBase

class GroqClient:
    """Groq - FREE extremely fast LLM API"""
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")  # FREE at console.groq.com
        self.base_url = "https://api.groq.com/openai/v1"
    
    async def agricultural_chat(self, question: str, language: str = "en") -> Dict:
        """FREE ultra-fast LLM responses"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = {
                "en": "You are an expert agricultural advisor for Indian farmers. Provide practical, actionable advice in simple language.",
                "hi": "आप भारतीय किसानों के लिए एक विशेषज्ञ कृषि सलाहकार हैं। सरल भाषा में व्यावहारिक सलाह दें।"
            }
            
            payload = {
                "model": "llama3-8b-8192",  # FREE model
                "messages": [
                    {"role": "system", "content": system_prompt.get(language, system_prompt["en"])},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/chat/completions", 
                                      headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "response": result["choices"][0]["message"]["content"],
                            "model": "Groq Llama3-8B (FREE)",
                            "speed": "Ultra-fast"
                        }
                    else:
                        return {"success": False, "error": f"Groq API Error: {response.status}"}
                        
        except Exception as e:
            return {"success": False, "error": str(e)}

class HuggingFaceFreeClient:
    """Hugging Face FREE Inference API"""
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")  # FREE at huggingface.co
        self.base_url = "https://api-inference.huggingface.co/models"
    
    async def query_free_models(self, question: str) -> Dict:
        """Query multiple FREE agricultural models"""
        
        free_models = [
            "microsoft/DialoGPT-medium",
            "facebook/blenderbot-400M-distill", 
            "microsoft/GODEL-v1_1-base-seq2seq",
            "google/flan-t5-base"
        ]
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        for model in free_models:
            try:
                url = f"{self.base_url}/{model}"
                payload = {
                    "inputs": f"Agricultural Question: {question}\nExpert Answer:",
                    "parameters": {"max_new_tokens": 150, "temperature": 0.7}
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            result = await response.json()
                            if result and not isinstance(result, dict) or not result.get('error'):
                                return {
                                    "success": True,
                                    "response": result[0]["generated_text"] if isinstance(result, list) else str(result),
                                    "model": f"HF-{model.split('/')[-1]} (FREE)",
                                    "cost": "FREE"
                                }
            except Exception as e:
                continue
        
        return {"success": False, "error": "All HF free models unavailable"}

class OllamaLocalClient:
    """Ollama - FREE local models"""
    def __init__(self):
        self.base_url = "http://localhost:11434"  # Local Ollama instance
    
    async def query_local_model(self, question: str) -> Dict:
        """Query FREE local Ollama models"""
        try:
            # Try common free models
            models = ["llama3.2:1b", "phi3:mini", "qwen2.5:0.5b"]
            
            for model in models:
                try:
                    payload = {
                        "model": model,
                        "prompt": f"You are an agricultural expert. Answer this farming question concisely: {question}",
                        "stream": False
                    }
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.post(f"{self.base_url}/api/generate", 
                                              json=payload) as response:
                            if response.status == 200:
                                result = await response.json()
                                return {
                                    "success": True,
                                    "response": result["response"],
                                    "model": f"Ollama-{model} (LOCAL/FREE)",
                                    "cost": "FREE (Local)"
                                }
                except Exception:
                    continue
            
            return {"success": False, "error": "No local models available"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

class GoogleTranslateFree:
    """Google Translate FREE API"""
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")  # FREE tier: 500K chars/month
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
    
    async def translate_text(self, text: str, target_language: str, source_language: str = "auto") -> Dict:
        """FREE translation service"""
        try:
            params = {
                "key": self.api_key,
                "q": text,
                "target": target_language,
                "source": source_language
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        translated_text = result["data"]["translations"][0]["translatedText"]
                        return {
                            "success": True,
                            "translated_text": translated_text,
                            "detected_language": result["data"]["translations"][0].get("detectedSourceLanguage"),
                            "cost": "FREE (500K chars/month)"
                        }
                    else:
                        return {"success": False, "error": f"Translation API Error: {response.status}"}
                        
        except Exception as e:
            return {"success": False, "error": str(e)}

class FreeAIOrchestrator:
    """Orchestrates all FREE AI services"""
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.groq_client = GroqClient()
        self.hf_client = HuggingFaceFreeClient()
        self.ollama_client = OllamaLocalClient()
        self.translator = GoogleTranslateFree()
    
    async def generate_response_free(self, question: str, language: str = "en") -> Dict:
        """Generate response using only FREE services"""
        
        # Step 1: Knowledge Base (LOCAL/FREE - highest priority)
        knowledge_results = self.knowledge_base.search_knowledge(question, top_k=3)
        
        if knowledge_results and knowledge_results[0]['confidence'] > 0.8:
            best_match = knowledge_results[0]
            
            # Translate if needed (FREE)
            response_text = best_match['answer']
            if language == 'hi' and not self.is_hindi_text(response_text):
                translation = await self.translator.translate_text(response_text, 'hi')
                if translation["success"]:
                    response_text = translation["translated_text"]
            
            return {
                "response": response_text,
                "confidence": best_match['confidence'],
                "model_used": "Knowledge Base (FREE)",
                "source": "Agricultural Expert Knowledge",
                "cost": "FREE",
                "success": True
            }
        
        # Step 2: Groq (FREE, ultra-fast)
        groq_result = await self.groq_client.agricultural_chat(question, language)
        if groq_result["success"]:
            return {
                "response": groq_result["response"],
                "confidence": 0.75,
                "model_used": groq_result["model"],
                "source": "Groq FREE API",
                "cost": "FREE",
                "success": True
            }
        
        # Step 3: Local Ollama (FREE)
        ollama_result = await self.ollama_client.query_local_model(question)
        if ollama_result["success"]:
            return {
                "response": ollama_result["response"],
                "confidence": 0.7,
                "model_used": ollama_result["model"],
                "source": "Local AI Model",
                "cost": "FREE",
                "success": True
            }
        
        # Step 4: Hugging Face Free (FREE)
        hf_result = await self.hf_client.query_free_models(question)
        if hf_result["success"]:
            return {
                "response": hf_result["response"],
                "confidence": 0.65,
                "model_used": hf_result["model"],
                "source": "Hugging Face FREE",
                "cost": "FREE",
                "success": True
            }
        
        # Step 5: Knowledge Base Fallback (always available)
        if knowledge_results:
            return {
                "response": f"Based on similar agricultural practices: {knowledge_results[0]['answer']}",
                "confidence": 0.6,
                "model_used": "Knowledge Base Fallback (FREE)",
                "source": "Agricultural Knowledge",
                "cost": "FREE",
                "success": True
            }
        
        # Ultimate fallback
        return {
            "response": "Please contact your local Krishi Vigyan Kendra (KVK) for expert agricultural guidance.",
            "confidence": 0.3,
            "model_used": "Referral Service (FREE)",
            "source": "Agricultural Extension Network",
            "cost": "FREE",
            "success": True
        }
    
    def is_hindi_text(self, text: str) -> bool:
        """Check if text contains Hindi characters"""
        return any('\u0900' <= char <= '\u097F' for char in text)