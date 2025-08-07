#!/usr/bin/env python3

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from services.generation_service import gen_cover_letter, gen_interview_questions, answer_query

def test_all():
    print("🌟 DeepSeek Complete Test")
    print("=" * 50)
    
    # Test 1: Q&A
    print("\n1️⃣ Testing Q&A with Resume:")
    try:
        result = answer_query("What is the person's name?")
        print(f"✅ Answer: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Cover Letter
    print("\n2️⃣ Testing Cover Letter Generation:")
    try:
        cover_letter = gen_cover_letter("We are looking for a Python developer with ML experience.")
        print(f"✅ Cover Letter:\n{cover_letter}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Interview Questions
    print("\n3️⃣ Testing Interview Questions:")
    try:
        questions = gen_interview_questions("Machine Learning Engineer")
        print(f"✅ Questions:\n{questions}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_all()
