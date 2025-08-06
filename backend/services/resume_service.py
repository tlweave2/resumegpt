# backend/services/resume_service.py
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class ResumeProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_resume(self, file_path: str):
        """Load and chunk resume from PDF or DOCX"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and use appropriate loader
        if file_path.lower().endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.lower().endswith(('.docx', '.doc')):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Use PDF or DOCX.")
        
        # Load and split documents
        documents = loader.load()
        chunked_docs = self.text_splitter.split_documents(documents)
        
        print(f"✅ Loaded {len(documents)} pages, split into {len(chunked_docs)} chunks")
        return chunked_docs
    
    def preview_chunks(self, chunks, num_preview=3):
        """Preview first few chunks for debugging"""
        for i, chunk in enumerate(chunks[:num_preview]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Content: {chunk.page_content[:200]}...")
            print(f"Metadata: {chunk.metadata}")

# Quick test function
if __name__ == "__main__":
    processor = ResumeProcessor()
    # Replace with your resume path
    chunks = processor.load_resume("sample_resume.pdf")
    processor.preview_chunks(chunks)