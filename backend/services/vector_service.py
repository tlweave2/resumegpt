# backend/services/vector_service.py
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class VectorService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = None
    
    def create_vector_store(self, documents):
        """Create FAISS vector store from documents"""
        if not documents:
            raise ValueError("No documents provided")
        
        print(f"🚀 Creating embeddings for {len(documents)} document chunks...")
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        print("✅ Vector store created successfully!")
        return self.vector_store
    
    def save_vector_store(self, save_path="data/vector_store"):
        """Save FAISS index to disk"""
        if not self.vector_store:
            raise ValueError("No vector store to save")
        
        os.makedirs(save_path, exist_ok=True)
        self.vector_store.save_local(save_path)
        print(f"💾 Vector store saved to {save_path}")
    
    def load_vector_store(self, load_path="data/vector_store"):
        """Load FAISS index from disk"""
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Vector store not found at {load_path}")
        
        self.vector_store = FAISS.load_local(
            load_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"📂 Vector store loaded from {load_path}")
        return self.vector_store
    
    def search(self, query: str, k: int = 3):
        """Search for most similar document chunks"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        results = self.vector_store.similarity_search(query, k=k)
        print(f"🔍 Found {len(results)} relevant chunks for: '{query}'")
        return results
    
    def search_with_scores(self, query: str, k: int = 3):
        """Search with similarity scores"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results

# Quick test function
if __name__ == "__main__":
    from resume_service import ResumeProcessor
    
    # Load documents
    processor = ResumeProcessor()
    chunks = processor.load_resume("sample_resume.pdf")
    
    # Create vector store
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    # Test search
    results = vector_service.search("Python programming experience")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}: {doc.page_content[:200]}...")