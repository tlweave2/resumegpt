# ResumeGPT with DeepSeek Integration

This project has been updated to use DeepSeek's API as the primary language model, with OpenAI as a fallback option.

## 🚀 Setup

### 1. Environment Variables

Create a `.env` file in the project root with your DeepSeek API key:

```bash
# DeepSeek API Configuration (Primary)
DEEPSEEK_API_KEY=sk-a8b08015b048431a9efd8423fa7f5cc8

# OpenAI API Key (Fallback - Optional)
OPENAI_API_KEY=your_openai_key_here
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## 🔧 Features

### 1. **Resume Processing & Q&A**
- Upload PDF, DOCX, or TXT resume files
- Uses DeepSeek for intelligent question answering about resume content
- Embeddings with fallback to simple text-based approach

### 2. **Cover Letter Generation**
- Generate personalized cover letters using DeepSeek
- Input: Job description
- Output: Tailored cover letter based on resume content

### 3. **Interview Questions**
- Generate relevant interview questions using DeepSeek
- Input: Job role/position
- Output: 5 customized interview questions

## 🧪 Testing

### Quick Test
```bash
cd backend
python test_deepseek.py
```

### Full Test Suite
```bash
cd backend/tests
python test_rag.py
```

## 📁 Project Structure

```
backend/
├── services/
│   ├── deepseek_service.py      # DeepSeek LLM & Embeddings wrapper
│   ├── generation_service.py    # Cover letter & interview questions
│   ├── vector_service.py        # FAISS vector store management
│   ├── resume_service.py        # Resume processing (PDF/DOCX/TXT)
│   └── rag_service.py          # RAG system
├── tests/
│   └── test_rag.py             # Comprehensive test suite
└── requirements.txt
```

## 🔍 Key Components

### DeepSeek Service (`deepseek_service.py`)
- **DeepSeekLLM**: Custom LangChain LLM wrapper for DeepSeek API
- **DeepSeekEmbeddings**: Custom embeddings with fallback
- Compatible with OpenAI Python SDK

### Generation Service (`generation_service.py`)
- Uses DeepSeek as primary LLM with OpenAI fallback
- Functions: `answer_query()`, `gen_cover_letter()`, `gen_interview_questions()`

### Vector Service (`vector_service.py`)
- FAISS vector store for semantic search
- DeepSeek embeddings with simple text-based fallback
- Functions: `build_faiss_index()`, `load_faiss_index()`

## 🚦 Usage Examples

### 1. Initialize and Query Resume
```python
from services.resume_service import ResumeProcessor
from services.vector_service import build_faiss_index
from services.generation_service import answer_query

# Load resume
processor = ResumeProcessor()
chunks = processor.load_resume("resume.pdf")

# Create vector store
vector_store = build_faiss_index(chunks)

# Ask questions
answer = answer_query("What programming languages does this person know?")
print(answer)
```

### 2. Generate Cover Letter
```python
from services.generation_service import gen_cover_letter

job_description = """
We are seeking a Senior Python Developer with experience in 
machine learning and web development using Django and React.
"""

cover_letter = gen_cover_letter(job_description)
print(cover_letter)
```

### 3. Generate Interview Questions
```python
from services.generation_service import gen_interview_questions

questions = gen_interview_questions("Senior Software Engineer")
print(questions)
```

## 🛠 API Endpoints (FastAPI)

### Start the Server
```bash
cd backend
uvicorn main:app --reload
```

### Available Endpoints
- `POST /upload` - Upload and process resume
- `GET /ask?q=question` - Ask questions about the resume
- `POST /generate-cover-letter` - Generate cover letter
- `POST /generate-interview-questions` - Generate interview questions

## 🎯 Key Benefits of DeepSeek Integration

1. **Cost-Effective**: DeepSeek offers competitive pricing
2. **High Performance**: Strong reasoning capabilities
3. **Seamless Integration**: Drop-in replacement for OpenAI
4. **Fallback Support**: Automatic fallback to OpenAI if needed
5. **Custom Embeddings**: Tailored embedding approach with fallback

## 🔧 Troubleshooting

### Common Issues

1. **"DeepSeek embeddings not available"**
   - This is normal - the system falls back to simple text-based embeddings
   - Vector search still works effectively

2. **API Key Issues**
   - Ensure `.env` file is in the project root
   - Verify your DeepSeek API key is valid

3. **FAISS Index Not Found**
   - Run the resume processing first to create the vector store
   - Check that the `data/vector_store/` directory exists

### Debug Mode
Add this to your Python script for debugging:
```python
import os
os.environ["LANGCHAIN_VERBOSE"] = "true"
```

## 📝 Notes

- The system automatically prefers DeepSeek but gracefully falls back to OpenAI
- Embeddings use a custom fallback approach when DeepSeek embeddings aren't available
- All vector operations are persistent via FAISS
- The system supports PDF, DOCX, and TXT resume formats

## 🎉 Success! 

Your ResumeGPT is now powered by DeepSeek! The integration provides:
- ✅ Intelligent resume Q&A
- ✅ Personalized cover letter generation  
- ✅ Custom interview question creation
- ✅ Robust fallback mechanisms
- ✅ Cost-effective AI operations
