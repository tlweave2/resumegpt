# test_rag_fixed.py - Run from backend/tests/ directory
import os
import sys
from dotenv import load_dotenv

# Add the parent directory (backend) to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This gets us to backend/
sys.path.insert(0, parent_dir)

print(f"🔍 Current directory: {current_dir}")
print(f"🔍 Parent directory: {parent_dir}")
print(f"🔍 Python path: {sys.path[:3]}")

# Now import from the services module
try:
    from services.resume_service import load_resume
    from services.vector_service import build_faiss_index, load_faiss_index
    from services.generation_service import answer_query, gen_cover_letter, gen_interview_questions
    print("✅ Imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Checking if services directory exists...")
    services_path = os.path.join(parent_dir, 'services')
    print(f"Services path: {services_path}")
    print(f"Services exists: {os.path.exists(services_path)}")
    if os.path.exists(services_path):
        print("Files in services:")
        for f in os.listdir(services_path):
            print(f"  - {f}")
    sys.exit(1)

def main():
    """Complete RAG system test"""
    # Load environment variables from project root
    env_path = os.path.join(parent_dir, '..', '.env')  # Go up to project root
    load_dotenv(env_path)
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found")
        print(f"Looking for .env file at: {env_path}")
        print("Please create a .env file in the project root with: OPENAI_API_KEY=your_key_here")
        return
    
    print("🚀 Starting ResumeGPT RAG System Test")
    print("=" * 50)
    
    # Step 1: Load Resume
    print("\n1️⃣ Loading Resume...")
    resume_path = input("Enter path to your resume (PDF/DOCX) or press Enter for sample: ").strip()
    
    if not resume_path:
        # Create sample resume in data directory
        create_sample_resume()
        resume_path = os.path.join(parent_dir, "sample_resume.pdf")
    
    if not os.path.exists(resume_path):
        print(f"❌ File not found: {resume_path}")
        return
    
    try:
        # Use existing function-based approach
        chunks = load_resume(resume_path)
        print(f"✅ Loaded {len(chunks)} document chunks")
        
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return
    
    # Step 2: Create Vector Store
    print("\n2️⃣ Creating Vector Store...")
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(parent_dir, "..", "data", "vector_store")
        os.makedirs(data_dir, exist_ok=True)
        
        # Use existing function to build FAISS index
        vector_store = build_faiss_index(chunks, os.path.join(data_dir, "faiss_index"))
        print("✅ Vector store created and saved successfully!")
        
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        print("Note: Make sure you have OPENAI_API_KEY set in your .env file")
        return
    
    # Step 3: Test RAG Functions
    print("\n3️⃣ Testing RAG System...")
    print("✅ RAG system ready!")
    
    # Pre-defined test questions
    test_questions = [
        "What programming languages are mentioned?",
        "What work experience is listed?", 
        "What are the key skills?",
        "What education background is mentioned?"
    ]
    
    print("\nRunning pre-defined tests:")
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: {question}")
        try:
            # Use existing answer_query function
            answer = answer_query(question)
            print(f"💬 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Interactive mode
    print("\n" + "="*50)
    print("🎯 Interactive Mode - Ask your own questions!")
    print("Commands: 'quit' to exit, 'cover' for cover letter, 'interview' for questions")
    
    while True:
        user_input = input("\n❓ Your question or command: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'cover':
            job_desc = input("📝 Enter job description: ").strip()
            if job_desc:
                try:
                    # Use existing gen_cover_letter function
                    cover_letter = gen_cover_letter(job_desc)
                    print(f"\n📄 Cover Letter:\n{cover_letter}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        elif user_input.lower() == 'interview':
            role = input("📝 Enter role/position: ").strip()
            if role:
                try:
                    # Use existing gen_interview_questions function
                    interview_prep = gen_interview_questions(role)
                    print(f"\n🎤 Interview Questions:\n{interview_prep}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        elif user_input:
            try:
                # Use existing answer_query function
                answer = answer_query(user_input)
                print(f"💬 Answer: {answer}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    print("\n🎉 RAG System Test Complete!")

def create_sample_resume():
    """Create a sample resume for testing"""
    sample_content = """John Doe - Software Engineer
    
    CONTACT: john.doe@email.com | LinkedIn: linkedin.com/in/johndoe
    
    EXPERIENCE:
    Senior Software Engineer at Tech Company (2020-2023)
    - Developed scalable web applications using Python, JavaScript, and React
    - Built REST APIs using Django and Flask frameworks  
    - Implemented CI/CD pipelines using Docker and GitHub Actions
    - Led a team of 3 junior developers on microservices architecture
    
    Software Developer at StartupCorp (2018-2020)
    - Created machine learning models using scikit-learn and TensorFlow
    - Designed database schemas in PostgreSQL and MongoDB
    - Collaborated with cross-functional teams using Agile methodology
    
    SKILLS:
    Programming Languages: Python, JavaScript, Java, SQL
    Frameworks: React, Django, Flask, Node.js
    Databases: PostgreSQL, MongoDB, Redis
    Tools: Docker, Git, AWS, Kubernetes
    
    EDUCATION:
    Bachelor of Science in Computer Science
    University of Technology (2014-2018)
    
    PROJECTS:
    E-commerce Platform: Built full-stack application with 10k+ users
    ML Recommendation System: Developed personalized product recommendations
    """
    
    try:
        # Try to create a simple PDF using reportlab
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = os.path.join(parent_dir, "sample_resume.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        
        # Split content into lines and add to PDF
        lines = sample_content.strip().split('\n')
        y = height - 50
        
        for line in lines:
            if y < 50:  # Start new page if needed
                c.showPage()
                y = height - 50
            c.drawString(50, y, line.strip())
            y -= 15
            
        c.save()
        print(f"📝 Created sample resume PDF: {pdf_path}")
        
    except ImportError:
        # Fallback: create text file and convert with pypdf2
        txt_path = os.path.join(parent_dir, "sample_resume.txt")
        with open(txt_path, 'w') as f:
            f.write(sample_content)
        print(f"📝 Created sample resume text file: {txt_path}")
        print("Note: Install reportlab with 'pip install reportlab' for PDF support")

if __name__ == "__main__":
    main()