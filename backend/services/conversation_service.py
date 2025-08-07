# backend/services/conversation_service.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from .deepseek_service import get_deepseek_llm
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ConversationService:
    def __init__(self, vector_store, memory_type="buffer"):
        # Initialize LLM
        try:
            self.llm = get_deepseek_llm()
            print("✅ Using DeepSeek LLM for conversations")
        except Exception as e:
            print(f"⚠️  DeepSeek not available ({e}), falling back to OpenAI")
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        
        self.vector_store = vector_store
        self.memory_type = memory_type
        self.memory = self._create_memory(memory_type)
        self.conversation_chain = self._create_conversation_chain()
    
    def _create_memory(self, memory_type="buffer"):
        """Create appropriate memory type"""
        if memory_type == "buffer":
            # Stores all conversation history
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"  # Important for ConversationalRetrievalChain
            )
        
        elif memory_type == "window":
            # Stores only last N exchanges
            return ConversationBufferWindowMemory(
                k=5,  # Keep last 5 exchanges
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
        
        elif memory_type == "summary":
            # Summarizes old conversations
            return ConversationSummaryBufferMemory(
                llm=self.llm,
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
                max_token_limit=1000  # Summarize when exceeding this
            )
        
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")
    
    def _create_conversation_chain(self):
        """Create conversational retrieval chain"""
        
        # Custom prompt for conversational resume Q&A
        custom_prompt = PromptTemplate.from_template(
            """You are a helpful assistant analyzing a resume. Use the conversation history and resume context to answer questions naturally.

Previous conversation:
{chat_history}

Resume context:
{context}

Current question: {question}

Instructions:
- Reference previous conversation when relevant (use phrases like "As I mentioned earlier" or "Building on what we discussed")
- Answer based on the resume content provided
- If information isn't in the resume, say "This information is not available in the resume"
- Be conversational and remember what was discussed earlier
- Use specific examples from the resume when possible
- If the question refers to something from earlier in the conversation (like "those skills" or "that company"), use the chat history to understand the reference

Answer:"""
        )
        
        # Create conversational retrieval chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": custom_prompt},
            return_source_documents=True,
            verbose=True  # Helpful for debugging
        )
        
        print("✅ Conversational RAG Chain initialized!")
        return chain
    
    def ask_question(self, question: str):
        """Ask a question with conversation context"""
        print(f"❓ Question: {question}")
        
        # Get response from conversational chain
        result = self.conversation_chain({"question": question})
        
        response = {
            "question": question,
            "answer": result["answer"],
            "source_chunks": [doc.page_content for doc in result.get("source_documents", [])],
            "chat_history": self.get_chat_history_formatted()
        }
        
        print(f"💬 Answer: {response['answer']}")
        return response
    
    def get_chat_history(self):
        """Get current conversation history (raw)"""
        return self.memory.chat_memory.messages
    
    def get_chat_history_formatted(self):
        """Get formatted conversation history"""
        messages = self.memory.chat_memory.messages
        formatted = []
        
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                human_msg = messages[i].content
                ai_msg = messages[i + 1].content
                formatted.append({
                    "question": human_msg,
                    "answer": ai_msg
                })
        
        return formatted
    
    def clear_memory(self):
        """Clear conversation history"""
        self.memory.clear()
        print("🧹 Conversation memory cleared!")
    
    def get_memory_summary(self):
        """Get summary of conversation (useful for debugging)"""
        messages = self.memory.chat_memory.messages
        return {
            "total_messages": len(messages),
            "memory_type": self.memory_type,
            "conversation_turns": len(messages) // 2,
            "last_messages": [msg.content for msg in messages[-4:]] if messages else [],
            "estimated_tokens": sum(len(msg.content) for msg in messages) // 4
        }
    
    def debug_memory(self):
        """Debug current memory state"""
        messages = self.memory.chat_memory.messages
        print(f"\n🔍 Memory Debug - {len(messages)} messages:")
        for i, msg in enumerate(messages):
            msg_type = "Human" if i % 2 == 0 else "AI"
            print(f"  {i}: {msg_type}: {msg.content[:80]}...")
    
    def switch_memory_type(self, new_memory_type):
        """Switch to a different memory type (clears existing memory)"""
        print(f"🔄 Switching from {self.memory_type} to {new_memory_type} memory")
        self.memory_type = new_memory_type
        self.memory = self._create_memory(new_memory_type)
        self.conversation_chain = self._create_conversation_chain()
        print("✅ Memory type switched successfully!")


# Test function for conversation memory
if __name__ == "__main__":
    from resume_service import ResumeProcessor
    from vector_service import VectorService
    
    # 1. Load resume
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    
    # 2. Create vector store
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    # 3. Initialize conversation service
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    # 4. Test conversation flow
    print("\n🎯 Testing Conversation Memory")
    print("=" * 40)
    
    # Test conversation with follow-ups
    test_conversation = [
        "What programming languages does this person know?",
        "Which of those languages has the most experience?",
        "What projects used Python?",
        "How many years of total experience does this person have?",
        "Based on our conversation, what makes this person qualified for a senior developer role?"
    ]
    
    for i, question in enumerate(test_conversation, 1):
        print(f"\n--- Turn {i} ---")
        response = conv_service.ask_question(question)
        print(f"Answer: {response['answer'][:150]}...")
    
    # Check memory
    print("\n📊 Final Memory Summary:")
    summary = conv_service.get_memory_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Debug memory
    conv_service.debug_memory()