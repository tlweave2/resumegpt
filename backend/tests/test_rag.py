# final_working_test.py - Uses your actual ResumeProcessor class
import os
import sys
from dotenv import load_dotenv

# Add the parent directory (backend) to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This gets us to backend/
sys.path.insert(0, parent_dir)

print(f"🔍 Current directory: {current_dir}")
print(f"🔍 Parent directory: {parent_dir}")

# Import your actual classes and functions
try:
    # Use the actual ResumeProcessor class
    from services.resume_service import ResumeProcessor
    print("✅ ResumeProcessor imported successfully!")
    
    # Check what's available in vector_service
    import services.vector_service as vs
    print(f"Available in vector_service: {[f for f in dir(vs) if not f.startswith('_')]}")
    
    # Check what's available in generation_service  
    import services.generation_service as gs
    print(f"Available in generation_service: {[f for f in dir(gs) if not f.startswith('_')]}")
    
    # Import the functions that actually exist
    from services.vector_service import build_faiss_index, load_faiss_index
    from services.generation_service import answer_query, gen_cover_letter, gen_interview_questions
    
    print("✅ All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def main():
    """Test the RAG system with your actual classes and functions"""
    # Load environment variables
    env_path = os.path.join(parent_dir, '..', '.env')
    load_dotenv(env_path)
    
    # Check DeepSeek API key first, then OpenAI as fallback
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if deepseek_key:
        print(f"✅ Found DeepSeek API key: {deepseek_key[:10]}...")
    elif openai_key:
        print(f"✅ Found OpenAI API key (fallback): {openai_key[:10]}...")
    else:
        print("❌ Error: Neither DEEPSEEK_API_KEY nor OPENAI_API_KEY found")
        print(f"Create a .env file at: {env_path}")
        print("With content:")
        print("DEEPSEEK_API_KEY=sk-a8b08015b048431a9efd8423fa7f5cc8")
        print("# OR as fallback:")
        print("OPENAI_API_KEY=your_openai_key_here")
        return
    
    print("\n🚀 Starting ResumeGPT RAG System Test")
    print("=" * 50)
    
    # Step 1: Create a test resume
    print("\n1️⃣ Creating Test Resume...")
    test_resume_path = create_test_resume()
    print(f"✅ Test resume created at: {test_resume_path}")
    
    # Step 2: Load Resume using ResumeProcessor class
    print("\n2️⃣ Loading Resume...")
    try:
        # Use your actual ResumeProcessor class
        processor = ResumeProcessor()
        chunks = processor.load_resume(test_resume_path)
        print(f"✅ Loaded {len(chunks)} document chunks")
        if chunks:
            print(f"Sample chunk preview: {chunks[0].page_content[:200]}...")
        
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return
    
    # Step 3: Create Vector Store
    print("\n3️⃣ Creating Vector Store...")
    try:
        # Make sure data directory exists
        data_dir = os.path.join(parent_dir, "..", "data", "vector_store")
        data_dir = os.path.abspath(data_dir)
        os.makedirs(data_dir, exist_ok=True)
        index_path = os.path.join(data_dir, "faiss_index")
        
        # Use your actual build_faiss_index function
        vector_store = build_faiss_index(chunks, index_path)
        print("✅ Vector store created and saved!")
        
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        print("Note: This requires a valid DeepSeek or OpenAI API key")
        return
    
    # Step 4: Test RAG Functions
    print("\n4️⃣ Testing RAG Functions...")
    
    # Test Q&A using your actual functions
    test_questions = [
        "What programming languages are mentioned in this resume?",
        "What is the work experience described?", 
        "What are the key technical skills?",
        "What projects are mentioned?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}: {question}")
        try:
            # Use your actual answer_query function
            answer = answer_query(question)
            print(f"💬 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error answering question: {e}")
    
    # Test Cover Letter Generation
    print(f"\n📄 Testing Cover Letter Generation...")
    try:
        job_desc = """We are seeking a Senior Software Engineer with strong Python experience, 
        web development skills, and experience with machine learning. The ideal candidate 
        will have experience with Django, React, and cloud platforms like AWS."""
        
        cover_letter = gen_cover_letter(job_desc)
        print(f"✅ Cover Letter Generated:")
        print(cover_letter)
    except Exception as e:
        print(f"❌ Cover letter generation error: {e}")
    
    # Test Interview Questions
    print(f"\n🎤 Testing Interview Questions...")
    try:
        role = "Senior Software Engineer"
        questions = gen_interview_questions(role)
        print(f"✅ Interview Questions Generated:")
        print(questions)
    except Exception as e:
        print(f"❌ Interview questions error: {e}")
    
    # Interactive mode
    print(f"\n🎯 Interactive Mode")
    print("Ask questions about the resume, or type 'quit' to exit:")
    
    while True:
        user_input = input("\n❓ Your question: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        elif user_input:
            try:
                answer = answer_query(user_input)
                print(f"💬 Answer: {answer}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("Please enter a question or 'quit' to exit.")
    
    print("\n🎉 RAG System Test Complete!")

def create_test_resume():
    """Create a simple test resume"""
    content = """John Smith - Senior Software Engineer

Contact Information:
Email: john.smith@email.com 
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith
Location: San Francisco, CA

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021-2024
• Developed scalable web applications using Python, Django, and React
• Built REST APIs serving over 100,000 daily active users
• Implemented machine learning recommendation systems using scikit-learn and TensorFlow
• Led cross-functional team of 4 developers in agile development environment
• Deployed applications on AWS using Docker and Kubernetes
• Achieved 99.9% uptime and reduced response times by 40%

Software Developer | StartupXYZ | 2019-2021
• Created full-stack web applications using JavaScript, Node.js, and MongoDB
• Designed and optimized database schemas for high-performance queries
• Collaborated with product managers to define technical requirements
• Implemented comprehensive automated testing suite with 90%+ code coverage
• Mentored 2 junior developers and conducted code reviews

Junior Developer | DevShop LLC | 2018-2019
• Built responsive websites using HTML, CSS, JavaScript, and PHP
• Integrated third-party APIs and payment processing systems
• Participated in daily standups and sprint planning meetings
• Contributed to open-source projects and internal tool development

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, Java, SQL, HTML, CSS, TypeScript
Frameworks & Libraries: Django, React, Node.js, Flask, Express.js, Vue.js
Databases: PostgreSQL, MongoDB, Redis, MySQL, SQLite
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform
Machine Learning: scikit-learn, TensorFlow, pandas, NumPy
Tools: Git, JIRA, Slack, Visual Studio Code, PyCharm

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2015-2019
GPA: 3.8/4.0
Relevant Coursework: Data Structures, Algorithms, Database Systems, Machine Learning

PROJECTS
E-Commerce Platform (2023)
• Built full-stack e-commerce application with payment processing using Stripe
• Implemented user authentication, shopping cart, and order management
• Technologies: Python, Django, React, PostgreSQL, AWS

Real-Time Analytics Dashboard (2022)  
• Created interactive dashboard for business metrics using D3.js and Python
• Processed over 1 million data points daily with real-time updates
• Technologies: Python, Flask, D3.js, Redis, WebSocket

Mobile Fitness App (2021)
• Developed React Native mobile application with 50,000+ downloads
• Integrated with fitness APIs and implemented social features
• Technologies: React Native, Node.js, MongoDB, Firebase

CERTIFICATIONS
• AWS Certified Solutions Architect (2023)
• Google Cloud Professional Data Engineer (2022)
• Certified Scrum Master (2021)"""

    # Create a text file (your ResumeProcessor should handle different file types)
    test_file_path = os.path.join(parent_dir, "test_resume.txt")
    
    # Try to create PDF if reportlab is available, otherwise create text file
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = os.path.join(parent_dir, "test_resume.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        lines = content.split('\n')
        y = 750
        
        for line in lines:
            if y < 50:
                c.showPage()
                y = 750
            # Handle long lines
            if len(line) > 80:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        c.drawString(50, y, current_line)
                        y -= 15
                        current_line = word + " "
                if current_line:
                    c.drawString(50, y, current_line)
                    y -= 15
            else:
                c.drawString(50, y, line)
                y -= 15
        
        c.save()
        return pdf_path
        
    except ImportError:
        # Fallback to text file
        with open(test_file_path, 'w') as f:
            f.write(content)
        return test_file_path

if __name__ == "__main__":
    main()