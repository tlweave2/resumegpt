# backend/services/rag_service.py
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from .deepseek_service import get_deepseek_llm
import os
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self, vector_store):
        # Try DeepSeek first, fallback to OpenAI
        try:
            self.llm = get_deepseek_llm()
            print("✅ Using DeepSeek LLM")
        except Exception as e:
            print(f"⚠️  DeepSeek not available ({e}), falling back to OpenAI")
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        self.vector_store = vector_store
        self.setup_qa_chain()
    
    def setup_qa_chain(self):
        """Initialize the QA chain with custom prompt"""
        # Custom prompt for resume Q&A
        qa_prompt = PromptTemplate(
            template="""You are a helpful assistant analyzing a resume. Use the following context to answer questions about the person's experience, skills, and background.

Context from resume:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the provided resume content
- If information isn't in the resume, say "This information is not available in the resume"
- Be specific and cite relevant experience when possible
- Keep responses concise but informative

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Create retrieval chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}  # Retrieve top 4 relevant chunks
            ),
            chain_type_kwargs={"prompt": qa_prompt},
            return_source_documents=True
        )
        print("✅ RAG QA Chain initialized!")
    
    def ask_question(self, question: str):
        """Ask a question about the resume"""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized")
        
        print(f"❓ Question: {question}")
        result = self.qa_chain({"query": question})
        
        response = {
            "question": question,
            "answer": result["result"],
            "source_chunks": [doc.page_content for doc in result["source_documents"]]
        }
        
        print(f"💬 Answer: {response['answer']}")
        return response
    
    def generate_cover_letter(self, job_description: str):
        """Generate a cover letter based on resume and job description"""
        cover_letter_prompt = f"""
        Based on the resume context provided, write a professional cover letter for this job:
        
        Job Description: {job_description}
        
        The cover letter should:
        - Highlight relevant experience from the resume
        - Match skills to job requirements
        - Be professional and engaging
        - Be 3-4 paragraphs long
        """
        
        result = self.qa_chain({"query": cover_letter_prompt})
        return result["result"]
    
    def get_interview_prep(self, job_description: str):
        """Generate interview preparation based on resume and job"""
        interview_prompt = f"""
        Based on the resume context, prepare for this job interview:
        
        Job Description: {job_description}
        
        Provide:
        1. 5 likely interview questions based on the job requirements
        2. Suggested answers using specific examples from the resume
        3. Questions to ask the interviewer
        
        Format your response clearly with numbered sections.
        """
        
        result = self.qa_chain({"query": interview_prompt})
        return result["result"]

# Complete RAG system test
if __name__ == "__main__":
    from resume_service import ResumeProcessor
    from vector_service import VectorService
    
    # 1. Load and process resume
    processor = ResumeProcessor()
    chunks = processor.load_resume("sample_resume.pdf")
    
    # 2. Create vector store
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    # 3. Initialize RAG
    rag = RAGService(vector_store)
    
    # 4. Test questions
    test_questions = [
        "What programming languages does this person know?",
        "What is their work experience?",
        "What projects have they worked on?",
        "What are their key skills?"
    ]
    
    for question in test_questions:
        response = rag.ask_question(question)
        print(f"\nQ: {question}")
        print(f"A: {response['answer']}")
        print("-" * 50)