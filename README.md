# 🌾 FarmLink: Agricultural Intelligence Assistant

> An agentic AI-powered platform that democratizes agricultural knowledge through intelligent assistance, voice input, and SMS support - completely FREE for farmers worldwide.

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://farmlink-omega.vercel.app)
[![Backend Status](https://img.shields.io/badge/backend-deployed-success)](https://farmlink-backend-iq4o.onrender.com)
[![Last Commit](https://img.shields.io/github/last-commit/surajsk2003/FARMLINK)](https://github.com/surajsk2003/FARMLINK)

---

## 📖 Table of Contents
- [🌾 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Live Demo](#-live-demo)
- [⚡ Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [📱 Usage](#-usage)
- [🎯 Problem Statement](#-problem-statement)
- [💡 Solution Approach](#-solution-approach)
- [🔮 Future Scope](#-future-scope)
- [🤝 Contributing](#-contributing)
- [👨‍💻 Author](#-author)

---

## 🌾 Overview

**FarmLink** addresses the critical information gap faced by farmers globally, particularly in developing regions. By leveraging cutting-edge agentic AI technology, it provides instant access to expert agricultural knowledge through multiple channels including voice input, text queries, and SMS integration.

### 🎯 Problem Statement
- **Information Gap**: Farmers lack timely access to scientific best practices
- **Language Barriers**: Limited multilingual agricultural resources
- **Accessibility**: Low literacy rates and limited internet connectivity
- **Cost**: Expensive agricultural consultation services
- **Coverage**: Understaffed traditional extension services

### 💡 Solution Approach
FarmLink uses **Retrieval-Augmented Generation (RAG)** architecture with agentic AI to deliver:
- Real-time, context-aware agricultural advice
- Multi-modal input (voice, text, SMS)
- 100% FREE service model
- Multilingual support (English/Hindi, expandable)
- Mobile-first responsive design

---

## ✨ Features

### 🧠 **AI Intelligence**
- **Agentic AI System**: Context-aware responses using advanced language models
- **Knowledge Retrieval**: FAISS-powered semantic search through agricultural databases
- **Multi-language Support**: English and Hindi with expansion capabilities

### 🎤 **Voice Integration**
- **Real-time Speech Recognition**: Web Speech API integration
- **Live Transcription**: See your words as you speak
- **Voice-to-Text**: Perfect for farmers with literacy challenges

### 📱 **SMS Integration**
- **Multi-provider Support**: TextLocal, Fast2SMS, Twilio Sandbox
- **Smart Routing**: Automatic fallback between SMS providers
- **Demo Mode**: Always-working demonstration capability

### 🌐 **Modern UI/UX**
- **Glass Morphism Design**: Modern, accessible interface
- **Responsive Design**: Mobile-first approach
- **Animated Interactions**: Smooth, professional user experience
- **Progressive Web App**: Installable on mobile devices

### 📚 **Agricultural Knowledge**
- **Comprehensive Database**: Covers crops, fertilizers, pests, diseases
- **Government Schemes**: PM-KISAN and other farmer benefits
- **Best Practices**: Scientific agricultural recommendations
- **Seasonal Guidance**: Timing for sowing, harvesting, and care

---

## 🛠️ Tech Stack

### **Frontend**
- **React.js** - Modern component-based UI framework
- **CSS3 & Custom Properties** - Advanced styling with glass morphism
- **Web Speech API** - Real-time voice recognition
- **Lucide React** - Beautiful, consistent icons
- **Vercel** - Global CDN deployment

### **Backend** 
- **FastAPI** - High-performance Python web framework
- **Pydantic** - Data validation and serialization
- **CORS Middleware** - Cross-origin resource sharing
- **Uvicorn** - ASGI server for production
- **Render.com** - Scalable cloud deployment

### **AI & ML**
- **Sentence Transformers** - Semantic text embeddings
- **FAISS** - Vector similarity search
- **Retrieval-Augmented Generation** - Context-aware AI responses
- **Multi-provider LLM Integration** - Flexible AI model support

### **Integration Services**
- **SMS Providers**: TextLocal, Fast2SMS, Twilio
- **Voice Recognition**: Browser-native Web Speech API
- **Translation Services**: Multi-language support system

---

## 🚀 Live Demo

### **🌐 Frontend Application**
**Live URL**: [https://farmlink-omega.vercel.app](https://farmlink-omega.vercel.app)

**Features to Try**:
- Ask agricultural questions in natural language
- Test voice input (click microphone icon)
- Try SMS demo with your phone number
- Switch between English/Hindi languages
- Explore quick question suggestions

### **🔧 Backend API**
**API URL**: [https://farmlink-backend-iq4o.onrender.com](https://farmlink-backend-iq4o.onrender.com)

**Endpoints**:
- `GET /health` - System health check
- `POST /ask` - Submit agricultural questions
- `GET /free-services` - Available service information
- `POST /sms/send` - SMS integration demo

---

## ⚡ Quick Start

### **Prerequisites**
```bash
Node.js 16+ 
Python 3.8+
Git
```

### **🔥 Installation**
```bash
# Clone the repository
git clone https://github.com/surajsk2003/FARMLINK.git
cd FARMLINK

# Setup Backend
cd agrisage-backend
pip install -r requirements.txt

# Setup Frontend  
cd ../agrisage-frontend
npm install
```

### **🚀 Running Locally**
```bash
# Terminal 1: Start Backend
cd agrisage-backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Frontend
cd agrisage-frontend
npm start
```

**Access Application**: `http://localhost:3000`

### **🐳 Docker Support** (Optional)
```bash
# Backend Docker
cd agrisage-backend
docker build -t farmlink-backend .
docker run -p 8000:8000 farmlink-backend

# Frontend builds automatically on Vercel
```

---

## 🏗️ Architecture

```
FarmLink Architecture (RAG-based)
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   AI Services   │
│   (React)       │    │   (FastAPI)      │    │                 │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ • Voice Input   │◄──►│ • RAG Pipeline   │◄──►│ • Vector Search │
│ • Modern UI     │    │ • API Endpoints  │    │ • LLM Models    │
│ • SMS Demo      │    │ • CORS Handling  │    │ • Knowledge DB  │
│ • Responsive    │    │ • Multi-language │    │ • Embeddings    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Deployment    │    │   Integration    │    │   Data Layer    │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│ • Vercel CDN    │    │ • SMS Providers  │    │ • FAISS Index   │
│ • Render Cloud  │    │ • Voice APIs     │    │ • Vector Store  │
│ • Auto-deploy   │    │ • Translation    │    │ • Knowledge KB  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **📁 Project Structure**
```
FARMLINK/
├── 🌐 agrisage-frontend/          # React frontend application
│   ├── public/                    # Static assets (favicon, manifest)
│   ├── src/                      # Source code
│   │   ├── App.js                # Main application component
│   │   ├── App.css               # Glass morphism styling
│   │   └── services/api.js       # Backend API integration
│   ├── package.json              # Frontend dependencies
│   └── vercel.json               # Vercel deployment config
├── 🔧 agrisage-backend/           # FastAPI backend application  
│   ├── app/                      # Application code
│   │   ├── main.py               # FastAPI application entry
│   │   ├── main_simple.py        # Lightweight version
│   │   ├── routers/              # API route handlers
│   │   └── services/             # Business logic services
│   ├── Dockerfile                # Container configuration
│   ├── requirements.txt          # Python dependencies
│   └── railway.json.backup       # Deployment configuration
└── 📚 README.md                  # Project documentation
```

---

## 📱 Usage

### **🗣️ Voice Input**
1. **Click microphone icon** in the question input area
2. **Allow microphone access** when prompted
3. **Speak your question** clearly in English or Hindi
4. **Watch live transcription** appear in real-time
5. **Click "Stop Recording"** when finished
6. **Submit your question** for AI processing

### **💬 Text Input**
1. **Type your agricultural question** in the text area
2. **Select language** (English/Hindi) from dropdown
3. **Click "Get FREE Answer"** to submit
4. **View AI response** with confidence score and source

### **📱 SMS Demo**
1. **Enter your phone number** with country code (+91XXXXXXXXXX)
2. **Type your question** in the main input area
3. **Click "Send SMS Demo"** button
4. **Receive confirmation** of SMS processing status

### **💡 Quick Questions**
- **Click any suggested question** in the sidebar
- **Questions auto-populate** in the main input
- **Submit directly** or modify before asking

### **📊 Response Analysis**
Each AI response includes:
- **✅ Confidence Score**: How certain the AI is about the answer
- **📚 Source Information**: Where the knowledge comes from  
- **🤖 Model Used**: Which AI system provided the response
- **⚡ Processing Time**: How quickly the response was generated
- **💰 Cost**: Always shows "FREE" for our service

---

## 🎯 Problem Statement Deep Dive

### **🌍 Global Agricultural Challenges**

**Information Accessibility**:
- 570+ million farms worldwide lack access to timely agricultural information
- Traditional extension services reach <30% of farmers in developing countries
- Language barriers prevent access to international best practices

**Economic Impact**:
- Suboptimal farming practices cause 20-40% yield losses annually  
- Information gaps cost farmers billions in potential income
- Lack of government scheme awareness limits benefit utilization

**Technology Gap**:
- 67% of farmers lack internet access for research
- Limited multilingual agricultural content
- Complex technical information not farmer-friendly

### **🎯 Target Users**

**Primary**: Small-scale farmers in developing regions
**Secondary**: Agricultural extension workers, rural communities
**Tertiary**: Agricultural students, researchers, policy makers

---

## 💡 Solution Approach

### **🤖 Agentic AI Architecture**

**Retrieval-Augmented Generation (RAG)**:
1. **Knowledge Ingestion**: Curated agricultural databases from trusted sources
2. **Vector Indexing**: Semantic search capabilities using FAISS
3. **Query Processing**: Multi-language natural language understanding  
4. **Context Retrieval**: Relevant information extraction from knowledge base
5. **Response Generation**: AI synthesis of contextual, actionable advice

**Multi-Modal Access**:
- **Voice**: Web Speech API for low-literacy accessibility
- **Text**: Traditional input with multilingual support
- **SMS**: Offline-capable service for remote areas

**Intelligence Features**:
- **Context Awareness**: Understands farming context and regional practices
- **Confidence Scoring**: Transparent reliability indicators
- **Source Attribution**: Traceable advice to trusted agricultural sources
- **Continuous Learning**: Expandable knowledge base architecture

---

## 🔮 Future Scope

### **🌱 Short-term Enhancements (3-6 months)**
- [ ] **Image Recognition**: Plant disease diagnosis from photos
- [ ] **Weather Integration**: Hyperlocal weather-based recommendations
- [ ] **Regional Languages**: Add 5+ Indian regional languages
- [ ] **Offline Mode**: Progressive Web App with offline capabilities
- [ ] **Farmer Profiles**: Personalized recommendations based on farm data

### **🌾 Medium-term Features (6-12 months)**  
- [ ] **IoT Integration**: Soil sensors and smart farming devices
- [ ] **Market Prices**: Real-time crop pricing and market intelligence
- [ ] **Community Platform**: Farmer-to-farmer knowledge sharing
- [ ] **Government Integration**: Direct scheme application assistance
- [ ] **Expert Consultation**: Video calls with agricultural experts

### **🌍 Long-term Vision (1-2 years)**
- [ ] **Global Expansion**: Support for 20+ languages and regions
- [ ] **Advanced AI**: Specialized models for different crop types
- [ ] **Blockchain**: Transparent supply chain and certification
- [ ] **Carbon Credits**: Sustainable farming practice tracking
- [ ] **Predictive Analytics**: AI-powered yield and risk predictions

---

## 🧩 Known Issues & Limitations

### **Current Limitations**
- **Voice Recognition**: Works best in Chrome, Edge, Safari browsers
- **SMS Integration**: Demo mode only (no actual SMS delivery in free tier)
- **Knowledge Base**: Limited to general agricultural practices (expanding)
- **Languages**: Currently supports English and Hindi only
- **Offline**: Requires internet connection for AI processing

### **🔧 Planned Fixes**
- Browser compatibility improvements for voice features
- Enhanced SMS provider integration with larger free tiers
- Expanded knowledge base with region-specific information
- Progressive Web App features for offline basic functionality

---

## 🤝 Contributing

We welcome contributions from the agricultural technology community!

### **🌟 Ways to Contribute**
- **Agricultural Knowledge**: Add region-specific farming practices
- **Language Support**: Translations and localized content
- **UI/UX Improvements**: Accessibility and design enhancements  
- **Technical Features**: Voice recognition, SMS integration improvements
- **Documentation**: Guides, tutorials, and example usage

### **📝 Contribution Process**
```bash
# Fork the repository
git fork https://github.com/surajsk2003/FARMLINK.git

# Create feature branch  
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m 'Add amazing agricultural feature'

# Push to branch
git push origin feature/amazing-feature

# Open Pull Request
```

### **🎯 Areas Needing Help**
- [ ] Regional agricultural practices database
- [ ] Multi-language translations  
- [ ] Mobile app development (React Native)
- [ ] Advanced AI model fine-tuning
- [ ] Government scheme database updates

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Why Open Source?**
- Agricultural knowledge should be freely accessible
- Community-driven improvements benefit all farmers  
- Transparent AI systems build trust with users
- Collaborative development accelerates innovation

---

## 🏆 Recognition & Awards

**Capital One Launchpad 2025 Hackathon**
- Category: Agentic AI Solutions for Agriculture
- Focus: High-impact societal applications of AI technology
- Theme: Democratizing agricultural knowledge through intelligent systems

---

## 👨‍💻 Author

**Suraj Kumar**  
*B.Tech Computer Science*  
*National Institute of Technology Karnataka (NITK), Surathkal*

### **🌐 Connect With Me**
- **Portfolio**: [https://surajsk2003.github.io/Suraj.in/](https://surajsk2003.github.io/Suraj.in/)
- **LinkedIn**: [https://www.linkedin.com/in/suraj-singh-96b45220a/](https://www.linkedin.com/in/suraj-singh-96b45220a/)
- **GitHub**: [https://github.com/surajsk2003](https://github.com/surajsk2003)
- **Email**: surajkumarsksk2000@gmail.com

### **🎓 Background**
Passionate about leveraging AI technology for social impact, particularly in agricultural development. Experienced in full-stack development, machine learning, and creating accessible technology solutions for underserved communities.

---

## 🙏 Acknowledgments

### **🌾 Agricultural Expertise**
- **Government Agricultural Portals**: PM-KISAN, Kisan Call Center resources
- **Agricultural Universities**: Best practices and research publications  
- **Extension Services**: Field-tested farming recommendations
- **Farmer Communities**: Real-world insights and feedback

### **🤖 Technology Partners**
- **Vercel**: Frontend hosting and global CDN
- **Render**: Backend deployment and scaling
- **Open Source Community**: React, FastAPI, and ML libraries
- **AI Research**: Transformer models and RAG architectures

### **💡 Inspiration**
Special thanks to farmers worldwide who inspired this project through their dedication to feeding the world despite facing information and resource challenges.

---

<div align="center">

### **🌾 Made with ❤️ for Farmers Worldwide**

**Star ⭐ this repo if FarmLink helped you or could help farmers in your community!**

[![GitHub stars](https://img.shields.io/github/stars/surajsk2003/FARMLINK?style=social)](https://github.com/surajsk2003/FARMLINK/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/surajsk2003/FARMLINK?style=social)](https://github.com/surajsk2003/FARMLINK/network/members)

---

**🚀 [Try FarmLink Live](https://farmlink-omega.vercel.app) | 📚 [Explore Code](https://github.com/surajsk2003/FARMLINK) | 🤝 [Contribute](CONTRIBUTING.md)**

*Empowering farmers through intelligent technology - one question at a time.*

</div>