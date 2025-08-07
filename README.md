# ResumeGPT 🧠

**AI-Powered Resume Intelligence with Conversation Memory**

Transform your resume into an intelligent conversational assistant that remembers context, generates personalized cover letters, and provides strategic career advice using advanced RAG (Retrieval-Augmented Generation) technology.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108+-red.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-orange.svg)](https://streamlit.io)

---

## 🎯 What ResumeGPT Does

ResumeGPT is a complete conversational AI system that understands your resume and provides intelligent career guidance. Unlike basic chatbots, it maintains conversation memory and provides contextually-aware responses.

### **Core Capabilities**

- 🗣️ **Natural Conversation**: Chat about your resume with full conversation memory
- 📄 **Multi-Format Support**: Upload PDF, DOCX, or TXT resumes
- 🧠 **Memory Types**: Choose from Buffer, Window, or Summary memory for different conversation styles
- ✍️ **Cover Letter Generation**: Create personalized cover letters for specific job descriptions
- 🎤 **Interview Preparation**: Generate role-specific interview questions and answers
- 🔍 **Semantic Search**: Find relevant information using AI-powered vector search
- 🤖 **LLM Integration**: Powered by DeepSeek with OpenAI fallback

---

## 🚀 Quick Demo

```bash
# 1. Start the system
git clone https://github.com/yourusername/resumegpt
cd resumegpt
pip install -r backend/requirements.txt

# 2. Set up environment
echo "DEEPSEEK_API_KEY=your_key_here" > .env

# 3. Launch backend and frontend
cd backend && uvicorn api.main:app --reload &
streamlit run frontend/streamlit_app.py
```

**Then**: Upload your resume and start chatting! 💬

---

## 💡 Example Conversations

### **Natural Follow-up Questions**
```
👤 User: "What programming languages do I know?"
🤖 ResumeGPT: "You have experience with Python, JavaScript, Java, and TypeScript..."

👤 User: "Which of those has the most experience?"
🤖 ResumeGPT: "Based on our previous discussion about your languages, Python has the most experience with 5+ years..."

👤 User: "What projects used Python?"
🤖 ResumeGPT: "Looking at the Python experience we discussed, you used it in your e-commerce platform, ML recommendation system, and analytics dashboard..."
```

### **Career Guidance**
```
👤 User: "Should I apply for senior roles?"
🤖 ResumeGPT: "Yes! With your 5 years of experience, leadership at TechCorp, and strong Python/AWS skills, you're well-qualified for senior positions. I'd recommend highlighting your team leadership and architecture experience."

👤 User: "Generate a cover letter for a Senior ML Engineer role"
🤖 ResumeGPT: "Based on your machine learning experience with TensorFlow and scikit-learn, here's a targeted cover letter..."
```

---

## 🏗️ Architecture

### **Technical Stack**
- **Backend**: FastAPI with async endpoints
- **Frontend**: Streamlit chat interface  
- **LLM**: DeepSeek (primary) + OpenAI (fallback)
- **Vector DB**: FAISS for semantic search
- **Memory**: LangChain conversation memory
- **Processing**: Multi-format document loading

### **System Components**
```
📱 Streamlit Frontend
    ↓ HTTP requests
🌐 FastAPI Backend
    ↓ calls
🧠 Conversation Service (Memory + RAG)
    ↓ retrieves from
📚 FAISS Vector Store (Resume embeddings)
    ↓ powered by
🤖 DeepSeek/OpenAI LLM
```

### **Key Services**
- **ResumeProcessor**: Multi-format document loading and chunking
- **VectorService**: FAISS vector store management with embeddings
- **ConversationService**: Memory-aware conversational AI
- **GenerationService**: Cover letter and interview question generation

---

## 📁 Project Structure

```
resumegpt/
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI server
│   ├── services/
│   │   ├── conversation_service.py  # Memory + RAG
│   │   ├── deepseek_service.py      # LLM integration
│   │   ├── generation_service.py    # Content generation
│   │   ├── resume_service.py        # Document processing
│   │   └── vector_service.py        # FAISS vector store
│   ├── tests/                   # Comprehensive test suite
│   └── requirements.txt
├── frontend/
│   └── streamlit_app.py         # Chat interface
├── data/
│   ├── uploads/                 # Resume uploads
│   └── vector_store/            # FAISS indices
├── .env                         # API keys
└── README.md
```

---

## ⚡ Getting Started

### **Prerequisites**
- Python 3.8+
- DeepSeek API key (or OpenAI as fallback)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resumegpt
   cd resumegpt
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in project root
   echo "DEEPSEEK_API_KEY=sk-your-deepseek-key-here" > .env
   
   # Optional: OpenAI fallback
   echo "OPENAI_API_KEY=sk-your-openai-key-here" >> .env
   ```

4. **Start the backend**
   ```bash
   cd backend
   uvicorn api.main:app --reload
   ```

5. **Start the frontend** (new terminal)
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

6. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## 🎮 Usage Guide

### **Upload Your Resume**
1. Use the sidebar file uploader
2. Supports PDF, DOCX, and TXT formats
3. Wait for processing confirmation

### **Start Chatting**
- Ask natural questions about your resume
- Have follow-up conversations with full context
- Try different memory types for various conversation styles

### **Generate Content**
- **Cover Letters**: Paste a job description and get a personalized cover letter
- **Interview Prep**: Enter a role and get targeted interview questions

### **Memory Types**
- **Buffer**: Remembers entire conversation (best for comprehensive discussions)
- **Window**: Keeps last 5 exchanges (good for focused topics)
- **Summary**: Summarizes old conversations (efficient for long chats)

---

## 🧪 Testing

### **Run Tests**
```bash
cd backend/tests
python test_rag.py              # Complete RAG system test
python test_conversion.py       # Memory and conversation tests
python test_all_deepseek.py     # DeepSeek integration tests
```

### **Interactive Testing**
```bash
# Test with your own resume
cd backend
python test_deepseek.py
```

---

## 🔧 Configuration

### **Memory Settings**
```python
# backend/services/conversation_service.py

# Buffer Memory (unlimited)
memory = ConversationBufferMemory(...)

# Window Memory (last N exchanges)  
memory = ConversationBufferWindowMemory(k=5, ...)

# Summary Memory (summarizes old conversations)
memory = ConversationSummaryBufferMemory(max_token_limit=1000, ...)
```

### **Chunking Strategy**
```python
# backend/services/resume_service.py
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,     # Adjust for your resume length
    chunk_overlap=200,   # Overlap for context preservation
    separators=["\n\n", "\n", " ", ""]
)
```

### **LLM Configuration**
```python
# backend/services/deepseek_service.py
# DeepSeek settings (primary)
model = "deepseek-chat"

# OpenAI fallback settings  
model = "gpt-3.5-turbo"
temperature = 0.7
```

---

## 🚀 API Reference

### **Core Endpoints**

#### **Upload Resume**
```http
POST /upload
Content-Type: multipart/form-data

# Response
{
  "status": "success",
  "message": "Resume processed successfully",
  "chunks_created": 15
}
```

#### **Ask Questions**
```http
POST /ask
Content-Type: application/json

{
  "question": "What are my key skills?",
  "memory_type": "buffer"
}

# Response
{
  "status": "success", 
  "answer": "Your key skills include...",
  "sources": ["chunk1", "chunk2"],
  "conversation_length": 3
}
```

#### **Generate Cover Letter**
```http
GET /cover-letter?job_desc=Senior Python Developer...

# Response
{
  "status": "success",
  "cover_letter": "Dear Hiring Manager..."
}
```

#### **Memory Management**
```http
POST /clear-memory
GET /memory-summary
```

### **Full API Documentation**
Visit http://localhost:8000/docs for interactive API documentation.

---

## 🔍 How It Works

### **Document Processing Pipeline**
1. **Upload**: Resume file received via API
2. **Loading**: Multi-format loader (PDF/DOCX/TXT)
3. **Chunking**: Intelligent text splitting with overlap
4. **Embedding**: Convert chunks to vector embeddings
5. **Storage**: Save in FAISS vector database

### **Conversation Flow**
1. **Question**: User asks about resume
2. **Retrieval**: Semantic search finds relevant chunks  
3. **Context**: Combine chunks with conversation history
4. **Generation**: LLM generates contextual response
5. **Memory**: Store exchange for future reference

### **Memory Management**
- **Buffer**: Stores all conversation history
- **Window**: Sliding window of recent exchanges  
- **Summary**: Summarizes older conversations to save tokens

---

## 🧠 LangChain Concepts Demonstrated

This project showcases comprehensive LangChain usage:

- ✅ **Document Loaders**: PDF, DOCX, TXT processing
- ✅ **Text Splitters**: Recursive character splitting with overlap
- ✅ **Embeddings**: DeepSeek + OpenAI fallback system
- ✅ **Vector Stores**: FAISS with persistent storage
- ✅ **Chains**: RetrievalQA, ConversationalRetrievalChain, LLMChain
- ✅ **Memory**: Buffer, Window, Summary memory types
- ✅ **Prompts**: Custom templates for different use cases
- ✅ **Retrievers**: Semantic similarity search
- ✅ **Custom LLM**: DeepSeek integration wrapper

---

## 🎯 Use Cases

### **Job Seekers**
- Understand your resume's strengths and weaknesses
- Generate tailored cover letters for applications
- Prepare for interviews with role-specific questions
- Get strategic career advice based on your experience

### **Career Changers**
- Analyze transferable skills for new industries
- Identify skill gaps and development areas
- Practice explaining your background for new roles

### **LangChain Learners**
- Complete working example of production RAG system
- Memory management patterns and best practices  
- Multi-format document processing
- Custom LLM integration techniques
- API design for AI applications

---

## 🔧 Troubleshooting

### **Common Issues**

#### **"Backend not connected"**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
cd backend && uvicorn api.main:app --reload
```

#### **"DeepSeek not available"**
```bash
# Check API key
echo $DEEPSEEK_API_KEY

# System will fall back to OpenAI automatically
echo "OPENAI_API_KEY=your-key" >> .env
```

#### **"FAISS index not found"**
```bash
# Upload a resume first to create the index
# Or check data/vector_store/ directory exists
mkdir -p data/vector_store
```

#### **Memory issues with long conversations**
- Switch to "window" or "summary" memory type
- Clear memory using the sidebar button
- Restart the conversation

### **Debug Mode**
```bash
# Enable verbose logging
export LANGCHAIN_VERBOSE=true

# Check conversation state
curl http://localhost:8000/debug/conversation-state
```

---

## 🤝 Contributing

We welcome contributions! This project is perfect for:

- LangChain enthusiasts learning advanced patterns
- Developers interested in conversational AI
- Career tech and HR tech innovations

### **Areas for Contribution**
- Additional document formats (LinkedIn export, etc.)
- Enhanced conversation memory strategies
- Better chunking strategies for different resume types
- Additional LLM provider integrations
- UI/UX improvements
- Performance optimizations

### **Development Setup**
```bash
# Fork the repo and clone your fork
git clone https://github.com/yourusername/resumegpt
cd resumegpt

# Create development branch
git checkout -b feature/your-feature

# Set up development environment
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt  # Dev dependencies

# Run tests before committing
cd backend/tests && python test_rag.py
```

---

## 📈 What's Next?

This is a foundation for much more! Planned enh
