import React, { useState, useEffect } from 'react';
import { Sprout, Mic, MicOff, Send, Loader, MessageCircle, Zap, Shield } from 'lucide-react';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [isRecording, setIsRecording] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [health, setHealth] = useState(null);
  const [history, setHistory] = useState([]);
  const [freeServices, setFreeServices] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');

  useEffect(() => {
    // Check API health and free services on startup
    apiService.getHealth().then(setHealth);
    apiService.getFreeServices().then(setFreeServices);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const result = await apiService.askQuestion(question, language);
      setResponse(result);
      
      // Add to history
      setHistory(prev => [{
        id: Date.now(),
        question,
        response: result,
        timestamp: new Date()
      }, ...prev].slice(0, 10)); // Keep last 10
      
    } catch (error) {
      setResponse({
        response: 'Sorry, there was an error processing your question. Please try again.',
        confidence: 0,
        model_used: 'Error Handler',
        source: 'System',
        success: false,
        cost: 'FREE'
      });
    } finally {
      setLoading(false);
    }
  };

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
      
      recognitionInstance.onstart = () => {
        setIsListening(true);
        setTranscript('');
      };
      
      recognitionInstance.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        setTranscript(finalTranscript || interimTranscript);
        if (finalTranscript) {
          setQuestion(prev => prev + ' ' + finalTranscript);
        }
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setIsRecording(false);
        
        const errorMessages = {
          'no-speech': 'No speech detected. Please try again.',
          'audio-capture': 'Microphone not accessible. Please check permissions.',
          'not-allowed': 'Microphone access denied. Please allow microphone access.',
          'network': 'Network error. Please check your internet connection.',
          'language-not-supported': 'Selected language not supported for voice input.'
        };
        
        alert(errorMessages[event.error] || 'Voice recognition error. Please try again.');
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
        setIsRecording(false);
      };
      
      setRecognition(recognitionInstance);
    }
  }, [language]);

  const handleVoiceRecord = () => {
    if (!recognition) {
      alert('Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    if (!isRecording) {
      // Start recording
      setIsRecording(true);
      recognition.lang = language === 'hi' ? 'hi-IN' : 'en-US';
      
      try {
        recognition.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setIsRecording(false);
        alert('Could not start voice recording. Please try again.');
      }
    } else {
      // Stop recording
      setIsRecording(false);
      setIsListening(false);
      recognition.stop();
    }
  };

  const handleSMSDemo = async () => {
    if (!phoneNumber || !question) {
      alert('Please enter both phone number and question first!');
      return;
    }

    // Basic phone number validation
    const cleanPhone = phoneNumber.replace(/\s/g, '');
    if (cleanPhone.length < 10 || !cleanPhone.match(/^\+?[\d\s-()]+$/)) {
      alert('Please enter a valid phone number (e.g., +91XXXXXXXXXX)');
      return;
    }

    try {
      setLoading(true);
      console.log('Sending SMS demo...', { phoneNumber: cleanPhone, question: question.substring(0, 50) });
      
      const result = await apiService.sendSMS(cleanPhone, question);
      console.log('SMS result:', result);
      
      if (result.success) {
        alert(`✅ SMS Demo Success!
        
📱 Phone: ${cleanPhone}
📝 Message: ${question.substring(0, 50)}...
🚀 Provider: ${result.details?.provider || 'Demo Mode'}
💰 Cost: ${result.details?.cost || 'FREE'}

${result.details?.note ? '\n📋 Note: ' + result.details.note : ''}`);
      } else {
        alert(`❌ SMS Demo Failed:
        
Error: ${result.error || result.message || 'Unknown error'}
        
Please check your inputs and try again.`);
      }
    } catch (error) {
      console.error('SMS Demo Error:', error);
      alert(`❌ SMS Demo Error:
      
Network issue: ${error.message}

Please check your connection and try again.`);
    } finally {
      setLoading(false);
    }
  };

  const QuickQuestions = () => {
    const questions = [
      { text: "What is the best fertilizer for wheat crop?", icon: "🌾" },
      { text: "How to control pests in cotton farming?", icon: "🐛" },
      { text: "When should I harvest my rice crop?", icon: "🍚" },
      { text: "What are PM-KISAN scheme benefits?", icon: "🏛️" },
      { text: "मेरी धान की फसल पीली हो रही है, क्या करूं?", icon: "🌱" },
      { text: "Best organic fertilizer for vegetables?", icon: "🥬" },
      { text: "How to manage tomato leaf curl disease?", icon: "🍅" },
      { text: "Best time to sow wheat in North India?", icon: "📅" }
    ];

    return (
      <div className="sidebar-card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span className="text-xl">💡</span>
          Quick Questions
        </h3>
        <div className="space-y-3 max-h-80 overflow-y-auto">
          {questions.map((q, index) => (
            <button
              key={index}
              onClick={() => setQuestion(q.text)}
              className="quick-question"
            >
              <span className="text-lg mr-3">{q.icon}</span>
              {q.text}
            </button>
          ))}
        </div>
      </div>
    );
  };

  const ResponseDisplay = ({ response }) => {
    if (!response) return null;

    const confidenceColor = response.confidence > 0.8 ? 'text-green-600' : 
                           response.confidence > 0.6 ? 'text-yellow-600' : 'text-red-600';
    const confidenceWidth = `${(response.confidence * 100)}%`;

    return (
      <div className="response-card">
        <div className="flex items-start justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-2xl">🌾</span>
            AgriSage AI Response
          </h3>
          <div className="flex flex-col items-end gap-2">
            <div className="flex items-center gap-2">
              <span className={`text-sm font-semibold ${confidenceColor}`}>
                {(response.confidence * 100).toFixed(1)}% Confidence
              </span>
              <span className="text-xs bg-gradient-to-r from-green-500 to-green-600 text-white px-3 py-1 rounded-full font-medium shadow-md">
                {response.cost || 'FREE'}
              </span>
            </div>
            <div className="confidence-bar w-24">
              <div 
                className="confidence-fill" 
                style={{ width: confidenceWidth }}
              ></div>
            </div>
          </div>
        </div>
        
        <div className="mb-6">
          <p className="text-gray-700 leading-relaxed text-lg font-medium">{response.response}</p>
        </div>
        
        <div className="flex flex-wrap gap-3 text-sm">
          <span className="bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 px-3 py-2 rounded-lg border border-blue-200">
            📚 Source: {response.source}
          </span>
          <span className="bg-gradient-to-r from-purple-50 to-purple-100 text-purple-700 px-3 py-2 rounded-lg border border-purple-200">
            🤖 Model: {response.model_used}
          </span>
          {response.processing_time && (
            <span className="bg-gradient-to-r from-orange-50 to-orange-100 text-orange-700 px-3 py-2 rounded-lg border border-orange-200">
              ⚡ {response.processing_time.toFixed(2)}s
            </span>
          )}
        </div>
      </div>
    );
  };

  const HistoryPanel = () => {
    if (history.length === 0) return null;

    return (
      <div className="glass-card p-6 mt-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span className="text-2xl">📜</span>
          Recent Questions
        </h3>
        <div className="space-y-4 max-h-80 overflow-y-auto">
          {history.slice(0, 5).map((item, index) => (
            <div key={item.id} className="group p-4 bg-gradient-to-r from-white/60 to-white/40 rounded-xl border border-white/20 cursor-pointer hover:bg-gradient-to-r hover:from-white/80 hover:to-white/60 transition-all hover:shadow-lg hover:scale-102 backdrop-blur-sm"
                 onClick={() => setQuestion(item.question)}>
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md">
                  {index + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-800 mb-2 line-clamp-2 group-hover:text-green-700 transition-colors">{item.question}</p>
                  <p className="text-xs text-gray-600 truncate mb-2 opacity-75">{item.response.response}</p>
                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-gradient-to-r from-green-500 to-green-600 text-white px-2 py-1 rounded-full font-medium shadow-sm">{item.response.cost}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const FreeServicesPanel = () => {
    if (!freeServices) return null;

    return (
      <div className="sidebar-card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span className="text-xl">⚡</span>
          100% FREE Services
        </h3>
        
        <div className="space-y-6">
          <div>
            <h4 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <span className="text-lg">📱</span>
              SMS Providers
            </h4>
            <div className="space-y-3">
              {Object.entries(freeServices.sms_providers || {}).map(([key, provider]) => (
                <div key={key} className="p-3 bg-gradient-to-r from-blue-50 to-indigo-100 rounded-lg border border-blue-200 transition-all hover:shadow-md hover:scale-105">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-blue-700 capitalize">{key}</span>
                    <span className="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded-full">{provider.region}</span>
                  </div>
                  <div className="text-sm text-blue-600 mt-1">{provider.limit}</div>
                </div>
              ))}
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <span className="text-lg">🤖</span>
              AI Models
            </h4>
            <div className="space-y-3">
              {Object.entries(freeServices.ai_providers || {}).map(([key, provider]) => (
                <div key={key} className="p-3 bg-gradient-to-r from-green-50 to-emerald-100 rounded-lg border border-green-200 transition-all hover:shadow-md hover:scale-105">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-green-700 capitalize">{key}</span>
                    <span className="text-xs bg-green-200 text-green-800 px-2 py-1 rounded-full">Active</span>
                  </div>
                  <div className="text-sm text-green-600 mt-1">{provider.limit || 'Unlimited'}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const SMSDemoPanel = () => {
    return (
      <div className="sidebar-card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span className="text-xl">📱</span>
          SMS Demo
        </h3>
        
        <div className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <span className="text-sm">📞</span>
              Phone Number (with country code)
            </label>
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="+91XXXXXXXXXX"
              className="w-full px-4 py-3 border-2 border-blue-100 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-300 transition-all bg-white/80 backdrop-blur-sm"
            />
          </div>
          
          <button
            onClick={handleSMSDemo}
            disabled={loading || !phoneNumber || !question}
            className="btn btn-secondary w-full"
          >
            <MessageCircle className="h-4 w-4" />
            Send SMS Demo
          </button>
          
          <div className="p-3 bg-gradient-to-r from-amber-50 to-orange-100 rounded-lg border border-amber-200">
            <p className="text-xs text-amber-700 font-medium flex items-center gap-2">
              <span className="text-sm">💡</span>
              Demo uses FREE SMS providers. Enter question above first.
            </p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="container mx-auto px-4 py-8 max-w-7xl">
          {/* Enhanced Header */}
          <header className="app-header">
            <div className="logo-container">
              <div className="logo-icon">
                <Sprout className="h-8 w-8 text-white" />
              </div>
              <h1 className="main-title">AgriSage AI</h1>
              <div className="logo-icon" style={{background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)'}}>
                <Shield className="h-6 w-6 text-white" />
              </div>
            </div>
            <p className="subtitle">
              Your 100% FREE Intelligent Agricultural Assistant
            </p>
            <p className="description">
              Ask questions about farming, get expert advice instantly • SMS support • Multi-language • AI-powered insights
            </p>
            
            {/* Enhanced Health Status */}
            {health && (
              <div className="status-container">
                <div className="status-badge status-healthy">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  API: {health.status} • v{health.version}
                </div>
                <div className="status-badge status-free">
                  <Zap className="h-4 w-4" />
                  100% FREE
                </div>
              </div>
            )}
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-3 space-y-6">
              {/* Language Selector */}
              <div className="glass-card p-6">
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  🌍 Select Language:
                </label>
                <select 
                  value={language} 
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-green-100 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-300 transition-all bg-white/80 backdrop-blur-sm"
                >
                  <option value="en">🇺🇸 English</option>
                  <option value="hi">🇮🇳 हिंदी (Hindi)</option>
                </select>
              </div>

              {/* Enhanced Question Input Form */}
              <div className="question-form-container">
                <form onSubmit={handleSubmit}>
                  <div className="space-y-6">
                    <div className="relative">
                      <textarea
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder={language === 'hi' ? 
                          "अपना कृषि प्रश्न यहाँ लिखें... 🌾" : 
                          "Ask your agricultural question here... 🌱"}
                        className="question-textarea"
                        rows="5"
                        disabled={loading}
                      />
                      {question.length > 0 && (
                        <div className="absolute bottom-4 right-4 text-sm text-gray-400">
                          {question.length}/1000
                        </div>
                      )}
                      
                      {/* Live Transcript Display */}
                      {isListening && transcript && (
                        <div className="absolute bottom-12 left-4 right-4 bg-gradient-to-r from-blue-50 to-indigo-100 p-3 rounded-lg border border-blue-200 backdrop-blur-sm">
                          <div className="flex items-center gap-2 mb-2">
                            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                            <span className="text-xs font-medium text-blue-700">Live Transcript:</span>
                          </div>
                          <p className="text-sm text-gray-700 italic">"{transcript}"</p>
                        </div>
                      )}
                    </div>
                    
                    {/* Voice Recording Instructions */}
                    {isRecording && (
                      <div className="mb-4 p-3 bg-gradient-to-r from-green-50 to-emerald-100 rounded-lg border border-green-200">
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                          <span className="text-sm font-medium text-green-700">Voice Recording Active</span>
                        </div>
                        <p className="text-xs text-green-600">
                          {language === 'hi' ? 'अपना प्रश्न बोलें। पूरा होने पर Stop Recording दबाएं।' : 'Speak your question clearly. Click "Stop Recording" when finished.'}
                        </p>
                      </div>
                    )}
                    
                    <div className="flex flex-col sm:flex-row gap-4">
                      <button
                        type="submit"
                        disabled={loading || !question.trim()}
                        className="btn btn-primary"
                      >
                        {loading ? (
                          <>
                            <Loader className="loading-spinner h-5 w-5" />
                            Processing Magic...
                          </>
                        ) : (
                          <>
                            <Send className="h-5 w-5" />
                            Get FREE Answer
                          </>
                        )}
                      </button>
                      
                      <button
                        type="button"
                        onClick={handleVoiceRecord}
                        className={`btn ${isRecording ? 'btn-accent relative' : 'btn-secondary'}`}
                      >
                        {isRecording ? (
                          <>
                            <MicOff className="h-5 w-5 animate-pulse" />
                            {isListening ? 'Listening...' : 'Stop Recording'}
                            {isListening && (
                              <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                            )}
                          </>
                        ) : (
                          <>
                            <Mic className="h-5 w-5" />
                            Voice Input
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </form>
              </div>

            {/* Response Display */}
            <ResponseDisplay response={response} />

            {/* History Panel */}
            <HistoryPanel />
          </div>

            {/* Enhanced Sidebar */}
            <div className="sidebar">
              <QuickQuestions />
              
              <FreeServicesPanel />
              
              <SMSDemoPanel />
              
              {/* Enhanced Features */}
              <div className="sidebar-card">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <span className="text-xl">✨</span>
                  Features
                </h3>
                <ul className="space-y-3 text-sm">
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    100% FREE service forever
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    Multi-language support (English/Hindi)
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    SMS integration worldwide
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    Voice input capability
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    Expert agricultural knowledge
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    Government schemes information
                  </li>
                  <li className="feature-item">
                    <div className="feature-icon"></div>
                    Crop-specific AI guidance
                  </li>
                </ul>
              </div>

              {/* Enhanced Contact Info */}
              <div className="sidebar-card">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <span className="text-xl">🆘</span>
                  Need More Help?
                </h3>
                <div className="space-y-4 text-sm text-gray-600">
                  <p className="font-medium text-gray-700">For complex issues, contact:</p>
                  <ul className="space-y-3">
                    <li className="flex items-center gap-3 p-2 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
                      <span className="text-lg">🏛️</span>
                      <div>
                        <div className="font-medium">Krishi Vigyan Kendra</div>
                        <div className="text-xs text-gray-500">Local agricultural center</div>
                      </div>
                    </li>
                    <li className="flex items-center gap-3 p-2 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
                      <span className="text-lg">📞</span>
                      <div>
                        <div className="font-medium">1800-180-1551</div>
                        <div className="text-xs text-gray-500">Kisan Call Center</div>
                      </div>
                    </li>
                    <li className="flex items-center gap-3 p-2 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
                      <span className="text-lg">🌐</span>
                      <div>
                        <div className="font-medium">pmkisan.gov.in</div>
                        <div className="text-xs text-gray-500">PM-KISAN Portal</div>
                      </div>
                    </li>
                    <li className="flex items-center gap-3 p-2 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg">
                      <span className="text-lg">📱</span>
                      <div>
                        <div className="font-medium">SMS: 51969</div>
                        <div className="text-xs text-gray-500">mKisan SMS service</div>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
