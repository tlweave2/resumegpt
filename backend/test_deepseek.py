#!/usr/bin/env python3

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from services.generation_service import answer_query
from services.vector_service import load_faiss_index

def test_deepseek():
    print("🧪 Testing DeepSeek Integration")
    print("=" * 40)
    
    # Test 1: Load vector store
    print("\n1️⃣ Testing vector store loading...")
    try:
        index_path = "/home/tim/AI/resumegpt/data/vector_store/faiss_index"
        print(f"Looking for index at: {index_path}")
        
        # Check if files exist
        if os.path.exists(index_path):
            print(f"✅ Directory exists: {index_path}")
            files = os.listdir(index_path)
            print(f"Files in directory: {files}")
        else:
            print(f"❌ Directory not found: {index_path}")
            return
        
        store = load_faiss_index(index_path)
        print("✅ Vector store loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Query with DeepSeek
    print("\n2️⃣ Testing query with DeepSeek...")
    try:
        question = "What programming languages are mentioned in this resume?"
        result = answer_query(question)
        print(f"✅ Question: {question}")
        print(f"✅ Answer: {result}")
        
    except Exception as e:
        print(f"❌ Error querying: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deepseek()
