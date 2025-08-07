# backend/services/resume_service.py
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
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
        """Load and chunk resume from PDF, DOCX, or TXT"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and use appropriate loader
        if file_path.lower().endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file_path.lower().endswith(('.docx', '.doc')):
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
        elif file_path.lower().endswith('.txt'):
            # Handle plain text files
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            documents = [Document(page_content=content, metadata={"source": file_path})]
        else:
            raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
        
        # Load and split documents
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