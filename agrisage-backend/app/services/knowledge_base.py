import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class AgricultureKnowledgeBase:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.setup_enhanced_knowledge()
        self.build_search_index()
    
    def setup_enhanced_knowledge(self):
        """Comprehensive agricultural knowledge base"""
        self.knowledge_base = [
            {
                "id": 0,
                "question": "How to grow crops?",
                "answer": "Complete guide to crop cultivation: 1) **Soil Preparation**: Test soil pH (6.0-7.5 ideal), add organic matter like compost or FYM, ensure proper drainage and tillage 2) **Seed Selection**: Choose high-quality, disease-resistant varieties suitable for your climate and soil type 3) **Sowing**: Follow proper spacing, depth, and timing based on crop requirements and local climate 4) **Water Management**: Provide adequate irrigation - avoid both water stress and waterlogging 5) **Nutrition**: Apply balanced fertilizers (NPK) based on soil test, supplement with micronutrients 6) **Pest & Disease Management**: Use integrated approach - cultural, biological, and chemical methods 7) **Weed Control**: Regular weeding, mulching, or herbicides to reduce competition 8) **Monitoring**: Regular field inspection for early problem detection 9) **Harvesting**: Harvest at proper maturity for maximum yield and quality 10) **Post-harvest**: Proper drying, storage, and handling to minimize losses",
                "keywords": ["crops", "cultivation", "farming", "agriculture", "grow", "planting", "general", "guide"],
                "category": "general_farming",
                "crop": "general",
                "language": "en"
            },
            {
                "id": 0.1,
                "question": "Basic steps for crop farming?",
                "answer": "Essential crop farming steps: 1) **Land Selection**: Choose suitable land with good soil, water availability, and proper drainage 2) **Crop Planning**: Select crops based on climate, market demand, and soil suitability 3) **Land Preparation**: Clear land, plow, harrow, and level the field for uniform planting 4) **Soil Testing**: Analyze soil for pH, nutrients, and organic matter content 5) **Seed Treatment**: Treat seeds with fungicides/insecticides to prevent diseases 6) **Sowing/Planting**: Plant at optimal time with proper spacing and depth 7) **Fertilization**: Apply organic manure and chemical fertilizers as needed 8) **Irrigation**: Provide water at critical growth stages - germination, flowering, grain filling 9) **Crop Protection**: Monitor and control pests, diseases, and weeds regularly 10) **Harvesting & Storage**: Harvest at right time and store properly to prevent losses",
                "keywords": ["farming", "steps", "agriculture", "cultivation", "basic", "beginner", "crop", "process"],
                "category": "general_farming",
                "crop": "general",
                "language": "en"
            },
            {
                "id": 0.2,
                "question": "फसल कैसे उगाएं?",
                "answer": "फसल उत्पादन की पूर्ण गाइड: 1) **भूमि तैयारी**: मिट्टी का pH परीक्षण करें (6.0-7.5 आदर्श), कंपोस्ट या गोबर खाद मिलाएं, जल निकासी की व्यवस्था करें 2) **बीज चयन**: उच्च गुणवत्ता के रोग प्रतिरोधी किस्मों का चुनाव करें 3) **बुवाई**: उचित समय, दूरी और गहराई में बीज बोएं 4) **जल प्रबंधन**: उचित सिंचाई करें - न अधिक न कम 5) **पोषण**: मिट्टी परीक्षण के अनुसार NPK उर्वरक दें 6) **कीट-रोग नियंत्रण**: एकीकृत प्रबंधन अपनाएं 7) **खरपतवार नियंत्रण**: नियमित निराई-गुड़ाई करें 8) **निगरानी**: नियमित खेत की जांच करें 9) **कटाई**: सही समय पर फसल काटें 10) **भंडारण**: उचित सुखाई और भंडारण करें",
                "keywords": ["फसल", "उगाना", "खेती", "कृषि", "farming", "crops", "cultivation"],
                "category": "general_farming",
                "crop": "general",
                "language": "hi"
            },
            {
                "id": 1,
                "question": "What is the best fertilizer for wheat crop?",
                "answer": "For wheat crop: 1) Apply NPK in ratio 120:60:40 kg/hectare 2) Use DAP (Di-ammonium phosphate) at sowing 3) Apply urea in 2-3 splits: 1/3 at sowing, 1/3 at CRI (Crown Root Initiation), 1/3 at jointing stage 4) Use zinc sulfate 25 kg/hectare if soil is deficient 5) Apply 10-15 tons FYM (Farm Yard Manure) before sowing 6) For organic farming: use vermicompost 5-8 tons/hectare",
                "keywords": ["wheat", "fertilizer", "NPK", "urea", "DAP", "nutrition", "organic"],
                "category": "fertilization",
                "crop": "wheat",
                "language": "en"
            },
            {
                "id": 2,
                "question": "How to control bollworm in cotton crop?",
                "answer": "Cotton bollworm (Helicoverpa armigera) control: 1) Use Bt cotton varieties for natural resistance 2) Install pheromone traps 5-10/hectare for early detection 3) Spray neem oil 5ml/liter water during evening 4) Release Trichogramma parasitoids 50,000/hectare weekly 5) Use light traps to attract and kill adult moths 6) For severe infestation: Emamectin benzoate 5% SG @ 220g/hectare 7) Maintain ETL (Economic Threshold Level): 2 larvae per plant 8) Crop rotation with non-host crops like wheat or sorghum",
                "keywords": ["cotton", "bollworm", "Helicoverpa", "pest", "control", "Bt cotton", "IPM"],
                "category": "pest_control",
                "crop": "cotton",
                "language": "en"
            },
            {
                "id": 3,
                "question": "मेरी धान की फसल पीली हो रही है, क्या करना चाहिए?",
                "answer": "धान की पत्तियां पीली होने के मुख्य कारण और उपचार: 1) नाइट्रोजन की कमी - यूरिया 130-150 kg/hectare छिड़काव करें, पानी में घोलकर स्प्रे करें 2) आयरन की कमी - फेरस सल्फेट 2.5% का घोल (25 ग्राम प्रति लीटर पानी) छिड़कें 3) जल भराव - खेत से अतिरिक्त पानी निकालें, जल निकासी की व्यवस्था करें 4) तना छेदक कीट - क्लोरपायरीफॉस 2ml प्रति लीटर पानी में मिलाकर स्प्रे करें 5) जिंक की कमी - जिंक सल्फेट 5 kg/hectare मिट्टी में मिलाएं 6) मिट्टी परीक्षण कराकर pH और पोषक तत्वों की जांच करें",
                "keywords": ["धान", "पीली", "rice", "yellowing", "nitrogen", "iron", "zinc", "fertilizer"],
                "category": "crop_health",
                "crop": "rice",
                "language": "hi"
            },
            {
                "id": 4,
                "question": "When should I harvest my rice crop?",
                "answer": "Rice harvesting timing indicators: 1) Visual signs: 80-85% grains turn golden yellow color 2) Moisture test: Grain moisture content should be 20-22% (bite test - grains should be hard, not soft) 3) Physical signs: Panicles bend downward due to grain weight 4) Time-based: Usually 25-35 days after flowering, depending on variety 5) Optimal timing: Early morning harvest (6-10 AM) for better grain quality 6) Maturity stages: Avoid harvesting too early (immature grains) or too late (shattering losses) 7) Weather consideration: Harvest before heavy rains to prevent quality loss 8) Yield loss: Delaying harvest results in 1-1.5% yield loss per day after optimal time",
                "keywords": ["rice", "harvest", "timing", "maturity", "moisture", "grain", "quality"],
                "category": "harvesting",
                "crop": "rice",
                "language": "en"
            },
            {
                "id": 5,
                "question": "What are PM-KISAN scheme benefits?",
                "answer": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) scheme benefits: 1) Financial support: ₹6000 per year direct cash transfer to farmer's bank account 2) Payment schedule: Amount paid in 3 equal installments of ₹2000 each (April-July, August-November, December-March) 3) Direct transfer: No intermediary involvement - money directly transferred through DBT (Direct Benefit Transfer) 4) Coverage: All landholding farmer families across India 5) No limit: No restriction on land size - small, marginal, and large farmers all eligible 6) Flexible use: Money can be used for any agricultural purpose - seeds, fertilizers, equipment, labor 7) Registration: Apply through CSC centers, Patwari, or online portal pmkisan.gov.in 8) Documents needed: Aadhaar card, bank account details, land records",
                "keywords": ["PM-KISAN", "pradhan mantri", "benefits", "cash", "transfer", "farmers", "DBT", "subsidy", "government"],
                "category": "government_schemes",
                "crop": "general",
                "language": "en"
            },
            {
                "id": 6,
                "question": "Why is rain important for rice cultivation?",
                "answer": "Rain importance for rice cultivation: 1) Water requirement: Rice requires 1200-1500mm annual rainfall for optimal growth - highest among cereals 2) Transplanting: Adequate rain needed for puddling and transplanting seedlings in flooded fields 3) Natural irrigation: Rain provides cost-free irrigation, reducing dependency on tube wells and canals 4) Grain filling: Sufficient moisture during grain filling stage (milky to dough stage) crucial for yield 5) Monsoon timing: Proper monsoon onset determines planting schedule and crop calendar 6) Nutrient availability: Rain helps in nutrient mobilization and uptake through roots 7) Temperature regulation: Rain cools down temperature, beneficial during hot weather 8) Pest control: Heavy rains can wash away certain pests naturally 9) Cost saving: Reduces irrigation costs significantly for farmers 10) Risk factor: However, excess rain during harvest can cause grain quality deterioration",
                "keywords": ["rain", "water", "rice", "cultivation", "monsoon", "irrigation", "paddy", "yield"],
                "category": "water_management",
                "crop": "rice",
                "language": "en"
            },
            {
                "id": 7,
                "question": "Best organic fertilizer for vegetables?",
                "answer": "Best organic fertilizers for vegetable cultivation: 1) Vermicompost: 5-8 tons/hectare - rich in NPK, micronutrients, and beneficial microorganisms 2) Farm Yard Manure (FYM): 20-25 tons/hectare - improves soil structure and water retention 3) Compost: 15-20 tons/hectare - decomposed organic matter with balanced nutrients 4) Neem cake: 200-500 kg/hectare - provides nutrition plus natural pest control properties 5) Bone meal: 100-200 kg/hectare - excellent source of phosphorus for root development 6) Bio-fertilizers: Rhizobium (for legumes), PSB (Phosphate Solubilizing Bacteria), Azotobacter for nitrogen fixation 7) Liquid organic manure: Cow urine, panchagavya - quick nutrient supply 8) Green manure: Dhaincha, sunhemp - grown and incorporated into soil",
                "keywords": ["organic", "fertilizer", "vegetables", "vermicompost", "FYM", "compost", "neem", "biofertilizer"],
                "category": "organic_farming",
                "crop": "vegetables",
                "language": "en"
            },
            {
                "id": 8,
                "question": "How to control pests in cotton farming?",
                "answer": "Integrated Pest Management (IPM) for cotton: 1) Resistant varieties: Use Bt cotton for bollworm resistance 2) Cultural practices: Crop rotation with wheat, sorghum, or pulses to break pest cycle 3) Monitoring: Install pheromone traps 5-10/hectare for bollworm detection 4) Biological control: Release Chrysoperla carnea (2500/hectare), Trichogramma (50,000/hectare weekly) 5) Mechanical control: Hand picking of larvae, use of light traps for adult moths 6) Botanical pesticides: Neem-based products for early instar larvae 7) Chemical control (last resort): When ETL exceeded - Emamectin benzoate for bollworm, Imidacloprid for sucking pests 8) Timing: Early morning or evening spray for better efficacy 9) Resistance management: Rotate different classes of insecticides",
                "keywords": ["cotton", "pest", "control", "IPM", "bollworm", "whitefly", "aphid", "thrips", "biological"],
                "category": "pest_control",
                "crop": "cotton",
                "language": "en"
            },
            {
                "id": 9,
                "question": "How to manage tomato leaf curl disease?",
                "answer": "Tomato leaf curl virus (ToLCV) management: 1) Resistant varieties: Use resistant cultivars like Arka Rakshak, Arka Samrat, Arka Ananya 2) Vector control: Control whitefly (Bemisia tabaci) - the virus vector 3) Physical barriers: Use yellow sticky traps @ 15-20/hectare to catch whiteflies 4) Chemical control: Spray Imidacloprid 17.8% SL @ 0.5ml/liter or Thiamethoxam @ 0.3g/liter 5) Cultural practices: Remove and destroy infected plants immediately, avoid ratooning 6) Preventive spray: Neem oil 5ml/liter every 10 days as preventive measure 7) Reflective mulch: Use silver/aluminum mulch to confuse whiteflies 8) Nursery care: Raise seedlings in insect-proof nets 9) Border crops: Plant marigold or basil as trap crops 10) Timing: Start spraying 15-20 days after transplanting",
                "keywords": ["tomato", "leaf curl", "virus", "ToLCV", "whitefly", "vector", "disease", "management"],
                "category": "disease_control",
                "crop": "tomato",
                "language": "en"
            },
            {
                "id": 10,
                "question": "Best time to sow wheat in North India?",
                "answer": "Optimal wheat sowing time in North India: 1) Ideal period: November 15 to December 15 - maximum yield potential 2) Soil temperature: 18-20°C is optimal for germination 3) Late sowing effects: After December 15, yield decreases by 1-1.5% per day delay 4) Early varieties: Can be sown till December 25 (varieties like PBW-343, HD-2967) 5) Irrigation conditions: November 15 - December 10 for irrigated areas 6) Rainfed conditions: October 25 - November 15 for rainfed areas 7) Soil moisture: Ensure adequate soil moisture before sowing 8) Preparation: Complete land preparation and apply basal fertilizers before sowing 9) Seed rate: 100 kg/hectare for timely sowing, 125 kg/hectare for late sowing 10) Depth: Sow at 5-6 cm depth for proper establishment",
                "keywords": ["wheat", "sowing", "time", "North India", "November", "December", "timing", "temperature"],
                "category": "crop_calendar",
                "crop": "wheat",
                "language": "en"
            }
        ]
    
    def build_search_index(self):
        """Build FAISS index for semantic search"""
        questions = [item['question'] for item in self.knowledge_base]
        self.embeddings = self.embedder.encode(questions)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        self.index.add(self.embeddings.astype('float32'))
    
    def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """Enhanced search for relevant answers"""
        query_embedding = self.embedder.encode([query])
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        
        # Check for exact keyword matches first
        query_lower = query.lower()
        general_queries = ["how to grow crops", "grow crops", "farming", "cultivation", "agriculture basics", "crop growing"]
        
        if any(general_term in query_lower for general_term in general_queries):
            # Prioritize general farming knowledge for broad queries
            for item in self.knowledge_base:
                if item.get('category') == 'general_farming':
                    results.append({
                        **item,
                        'similarity_score': 0.95,
                        'confidence': 0.95
                    })
                    break
        
        # Add semantic search results
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.knowledge_base):
                item = self.knowledge_base[idx]
                # Avoid duplicates
                if not any(r['id'] == item['id'] for r in results):
                    results.append({
                        **item,
                        'similarity_score': float(score),
                        'confidence': min(float(score * 1.2), 1.0)  # Boost confidence slightly
                    })
        
        # Sort by confidence and return top results
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results[:top_k]