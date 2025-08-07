# backend/services/vector_service.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from .deepseek_service import get_deepseek_embeddings
import os
from dotenv import load_dotenv

load_dotenv()

class VectorService:
    def __init__(self):
        # Try DeepSeek embeddings first, fallback to OpenAI
        try:
            self.embeddings = get_deepseek_embeddings()
            print("✅ Using DeepSeek embeddings")
        except Exception as e:
            print(f"⚠️  DeepSeek embeddings not available ({e}), falling back to OpenAI")
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


def get_embeddings():
    """Get the appropriate embeddings instance (DeepSeek preferred, OpenAI fallback)"""
    try:
        embeddings = get_deepseek_embeddings()
        print("✅ Using DeepSeek embeddings")
        return embeddings
    except Exception as e:
        print(f"⚠️  DeepSeek embeddings not available ({e}), falling back to OpenAI")
        from langchain.embeddings import OpenAIEmbeddings
        return OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


def build_faiss_index(documents, save_path="data/vector_store/faiss_index"):
    """Build and save FAISS index from documents"""
    if not documents:
        raise ValueError("No documents provided")
    
    print(f"🚀 Creating embeddings for {len(documents)} document chunks...")
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Normalize path and ensure directory exists
    save_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save the index
    vector_store.save_local(save_path)
    print(f"💾 Vector store saved to {save_path}")
    return vector_store


def load_faiss_index(load_path="data/vector_store/faiss_index"):
    """Load FAISS index from disk"""
    # Normalize path
    load_path = os.path.abspath(load_path)
    
    # Check if the directory exists (FAISS creates subdirectory)
    if os.path.isdir(load_path):
        faiss_file = os.path.join(load_path, "index.faiss")
    else:
        faiss_file = f"{load_path}.faiss"
    
    if not os.path.exists(faiss_file):
        raise FileNotFoundError(f"FAISS index not found at {load_path}")
    
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        load_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"📂 Vector store loaded from {load_path}")
    return vector_store


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