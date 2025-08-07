"""
Frontend Streamlit Chat Interface for ResumeGPT
This talks to the backend API instead of importing services directly
"""

import streamlit as st
import requests
import json
from typing import Dict, List, Optional

# Configuration
BACKEND_URL = "http://localhost:8000"  # Backend API URL

# Page config
st.set_page_config(
    page_title="ResumeGPT Chat",
    page_icon="🧠",
    layout="wide"
)

class BackendAPI:
    """Client for communicating with backend API"""
    
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
    
    def upload_resume(self, file_data, filename: str) -> Dict:
        """Upload resume to backend"""
        try:
            files = {"file": (filename, file_data, "application/octet-stream")}
            response = requests.post(f"{self.base_url}/upload", files=files)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def ask_question(self, question: str, memory_type: str = "buffer") -> Dict:
        """Ask a question with conversation memory"""
        try:
            data = {"question": question, "memory_type": memory_type}
            response = requests.post(f"{self.base_url}/ask", json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def clear_memory(self) -> Dict:
        """Clear conversation memory"""
        try:
            data = {"confirm": True}
            response = requests.post(f"{self.base_url}/clear-memory", json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def get_memory_summary(self) -> Dict:
        """Get memory usage summary"""
        try:
            response = requests.get(f"{self.base_url}/memory-summary")
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def generate_cover_letter(self, job_description: str) -> Dict:
        """Generate cover letter"""
        try:
            params = {"job_desc": job_description}
            response = requests.get(f"{self.base_url}/cover-letter", params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def generate_interview_questions(self, role: str) -> Dict:
        """Generate interview questions"""
        try:
            params = {"role": role}
            response = requests.get(f"{self.base_url}/interview", params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}
    
    def health_check(self) -> bool:
        """Check if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=3)
            return response.status_code == 200
        except:
            return False

# Initialize API client
api = BackendAPI()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'resume_loaded' not in st.session_state:
    st.session_state.resume_loaded = False
if 'backend_connected' not in st.session_state:
    st.session_state.backend_connected = False

def check_backend_connection():
    """Check if backend is available"""
    if api.health_check():
        st.session_state.backend_connected = True
        return True
    else:
        st.session_state.backend_connected = False
        return False

def load_resume(uploaded_file):
    """Load and process uploaded resume via API"""
    try:
        with st.spinner("📄 Uploading and processing resume..."):
            result = api.upload_resume(uploaded_file.getvalue(), uploaded_file.name)
        
        if "error" in result:
            st.error(f"Error: {result['error']}")
            return False
        
        st.session_state.resume_loaded = True
        st.session_state.chat_history = []
        return result
        
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")
        return False

def display_chat_history():
    """Display chat history with conversation context"""
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        
        for i, exchange in enumerate(st.session_state.chat_history):
            # Question
            with st.chat_message("user"):
                st.write(exchange['question'])
            
            # Answer
            with st.chat_message("assistant"):
                st.write(exchange['answer'])
                
                # Show sources in expander
                if exchange.get('sources'):
                    with st.expander(f"📚 Sources ({len(exchange['sources'])} chunks)"):
                        for j, source in enumerate(exchange['sources'][:2]):
                            st.text(f"Source {j+1}: {source[:200]}...")

def main():
    st.title("🧠 ResumeGPT Chat Interface")
    st.markdown("*Natural conversation about your resume with memory*")
    
    # Check backend connection
    if not check_backend_connection():
        st.error("🚨 **Backend not connected!**")
        st.markdown("""
        The backend API is not running. Please:
        1. Start the backend: `cd backend && python -m uvicorn api.main:app --reload`
        2. Verify it's running at http://localhost:8000
        3. Refresh this page
        """)
        return
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Backend status
        if st.session_state.backend_connected:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Disconnected")
        
        # Memory type selection
        memory_type = st.selectbox(
            "Memory Type",
            ["buffer", "window", "summary"],
            index=0,
            help="Buffer: Remembers everything\nWindow: Last 5 exchanges\nSummary: Summarizes old conversations"
        )
        
        # Resume upload
        st.header("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose your resume",
            type=['pdf', 'docx', 'txt'],
            help="Upload your resume to start chatting"
        )
        
        if uploaded_file and not st.session_state.resume_loaded:
            result = load_resume(uploaded_file)
            if result:
                st.success(f"✅ Resume processed!")
                if 'message' in result:
                    st.info(result['message'])
        
        # Memory controls (only show if resume loaded)
        if st.session_state.resume_loaded:
            st.header("🧠 Memory Status")
            
            # Get memory summary
            try:
                summary_result = api.get_memory_summary()
                if "error" not in summary_result and "memory_summary" in summary_result:
                    summary = summary_result["memory_summary"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Turns", summary.get('conversation_turns', 0))
                        st.metric("Type", summary.get('memory_type', 'unknown').title())
                    with col2:
                        st.metric("Tokens", summary.get('estimated_tokens', 0))
                        
                        # Progress bar for token usage
                        token_pct = min(summary.get('estimated_tokens', 0) / 4000, 1.0)
                        st.progress(token_pct)
                        
                        if token_pct > 0.75:
                            st.warning("⚠️ Memory getting full!")
                
            except Exception as e:
                st.error(f"Error getting memory status: {e}")
            
            # Clear memory button
            if st.button("🧹 Clear Memory", help="Clear conversation history"):
                try:
                    result = api.clear_memory()
                    if "error" not in result:
                        st.session_state.chat_history = []
                        st.success("Memory cleared!")
                        st.rerun()
                    else:
                        st.error(f"Error clearing memory: {result['error']}")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Additional tools
        if st.session_state.resume_loaded:
            st.header("🛠️ Resume Tools")
            
            # Cover letter generator
            with st.expander("📝 Cover Letter"):
                job_desc = st.text_area("Job Description", height=100)
                if st.button("Generate Cover Letter"):
                    if job_desc:
                        with st.spinner("Writing cover letter..."):
                            result = api.generate_cover_letter(job_desc)
                            if "error" not in result:
                                st.text_area("Cover Letter", result.get("cover_letter", ""), height=300)
                            else:
                                st.error(result["error"])
                    else:
                        st.warning("Please enter a job description")
            
            # Interview questions
            with st.expander("🎤 Interview Prep"):
                role = st.text_input("Role (e.g., 'Senior Python Developer')")
                if st.button("Generate Questions"):
                    if role:
                        with st.spinner("Preparing interview questions..."):
                            result = api.generate_interview_questions(role)
                            if "error" not in result:
                                st.text_area("Interview Questions", result.get("questions", ""), height=300)
                            else:
                                st.error(result["error"])
                    else:
                        st.warning("Please enter a role")
    
    # Main chat interface
    if not st.session_state.resume_loaded:
        st.info("👆 Please upload your resume in the sidebar to start chatting!")
        
        # Show example conversation
        st.markdown("### 💡 Example Conversation Flow")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Without Memory (Traditional Q&A):**")
            st.code("""
Q: What languages does this person know?
A: Python, JavaScript, Java...

Q: Which has the most experience?
A: I don't have context about which 
   languages you're referring to.
            """)
        
        with col2:
            st.markdown("**With Memory (Natural Conversation):**")
            st.code("""
Q: What languages does this person know?
A: Python, JavaScript, Java...

Q: Which has the most experience?
A: Based on our discussion about their 
   languages, Python has the most experience...
            """)
        
        st.markdown("### 🎯 Try These Questions:")
        example_questions = [
            "What programming languages does this person know?",
            "Which of those has the most experience?",
            "What projects used that language?",
            "How many years of total experience?",
            "What makes them qualified for a senior role?"
        ]
        
        for i, eq in enumerate(example_questions):
            st.markdown(f"**{i+1}.** {eq}")
        
    else:
        # Chat interface
        st.markdown("### 💭 Chat with Your Resume")
        
        # Question input using chat_input (more natural)
        question = st.chat_input("Ask anything about the resume...")
        
        if question:
            # Add user message to history immediately
            st.session_state.chat_history.append({
                'question': question,
                'answer': None,  # Will be filled when response comes
                'sources': []
            })
            # Show user message
            with st.chat_message("user"):
                st.write(question)
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = api.ask_question(question, memory_type)
                        if "error" in response:
                            st.error(f"Error: {response['error']}")
                            st.session_state.chat_history.pop()
                        elif 'answer' in response:
                            st.session_state.chat_history[-1]['answer'] = response['answer']
                            st.session_state.chat_history[-1]['sources'] = response.get('sources', [])
                            st.write(response['answer'])
                            if response.get('sources'):
                                with st.expander(f"📚 Sources ({len(response['sources'])} chunks)"):
                                    for i, source in enumerate(response['sources'][:2]):
                                        st.text(f"Source {i+1}: {source[:200]}...")
                        else:
                            st.error("Error: No answer returned from backend.")
                            st.session_state.chat_history.pop()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.session_state.chat_history.pop()
        
        # Display existing chat history
        if st.session_state.chat_history:
            st.markdown("---")
            for exchange in st.session_state.chat_history[:-1]:  # Don't show the last one (it's already shown above)
                if exchange['answer']:  # Only show complete exchanges
                    with st.chat_message("user"):
                        st.write(exchange['question'])
                    
                    with st.chat_message("assistant"):
                        st.write(exchange['answer'])
                        
                        if exchange.get('sources'):
                            with st.expander(f"📚 Sources"):
                                for i, source in enumerate(exchange['sources'][:2]):
                                    st.text(f"Source {i+1}: {source[:200]}...")

if __name__ == "__main__":
    main()
