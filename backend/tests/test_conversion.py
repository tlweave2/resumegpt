#!/usr/bin/env python3

import sys
import os
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from services.resume_service import ResumeProcessor
from services.vector_service import VectorService
from services.conversation_service import ConversationService

def test_basic_conversation():
    """Test basic conversation functionality"""
    print("🧠 Testing Basic Conversation Memory")
    print("=" * 50)
    
    # 1. Load resume
    print("\n1️⃣ Loading resume...")
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    print(f"✅ Loaded {len(chunks)} chunks")
    
    # 2. Create vector store
    print("\n2️⃣ Creating vector store...")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    print("✅ Vector store created")
    
    # 3. Test conversation
    print("\n3️⃣ Testing conversation with memory...")
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    # Basic conversation flow
    questions = [
        "What's this person's name?",
        "What programming languages do they know?",
        "Which of those languages appears most in their experience?",
        "What specific projects used that language?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n  Q{i}: {question}")
        response = conv_service.ask_question(question)
        print(f"  A{i}: {response['answer']}")
        
        # Show memory growth
        summary = conv_service.get_memory_summary()
        print(f"  📊 Memory: {summary['conversation_turns']} turns, ~{summary['estimated_tokens']} tokens")
    
    return conv_service

def test_memory_types():
    """Compare different memory types"""
    print("\n\n🔬 Testing Different Memory Types")
    print("=" * 50)
    
    # Load data once
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    memory_types = ["buffer", "window", "summary"]
    
    # Long conversation to test memory limits
    long_conversation = [
        "What's this person's name?",
        "What programming languages do they know?",
        "Tell me about their work experience",
        "What projects have they worked on?",
        "What's their educational background?",
        "What makes them qualified for a senior role?",
        "How do their skills compare to a typical developer?",
        "What would you recommend they improve on?"
    ]
    
    for memory_type in memory_types:
        print(f"\n🧪 Testing {memory_type.upper()} memory...")
        
        try:
            conv_service = ConversationService(vector_store, memory_type=memory_type)
            
            for i, question in enumerate(long_conversation, 1):
                print(f"  Q{i}: {question[:50]}...")
                response = conv_service.ask_question(question)
                print(f"  A{i}: {response['answer'][:80]}...")
                
                # Check memory after each question
                summary = conv_service.get_memory_summary()
                print(f"       Memory: {summary['conversation_turns']} turns, ~{summary['estimated_tokens']} tokens")
            
            # Final memory summary
            final_summary = conv_service.get_memory_summary()
            print(f"\n  📊 Final {memory_type} summary:")
            print(f"     Conversation turns: {final_summary['conversation_turns']}")
            print(f"     Total messages: {final_summary['total_messages']}")
            print(f"     Estimated tokens: {final_summary['estimated_tokens']}")
            
        except Exception as e:
            print(f"❌ Error with {memory_type} memory: {e}")
            import traceback
            traceback.print_exc()

def test_follow_up_understanding():
    """Test how well the system handles follow-up questions"""
    print("\n\n🎯 Testing Follow-up Question Understanding")
    print("=" * 50)
    
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    # Test conversation with ambiguous follow-ups
    test_scenarios = [
        {
            "name": "Pronoun Reference Test",
            "conversation": [
                "What programming languages does this person know?",
                "Which one is used most frequently?",
                "What projects used it?",
                "How many years of experience with that language?"
            ]
        },
        {
            "name": "Topic Continuation Test", 
            "conversation": [
                "Tell me about their work experience",
                "Which company was the most recent?",
                "What did they do there?",
                "How long did they work at that place?"
            ]
        },
        {
            "name": "Skills Deep Dive Test",
            "conversation": [
                "What technical skills do they have?",
                "Which of those skills are most advanced?",
                "Can you give examples of where they used those?",
                "How do those skills compare to industry standards?"
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🔍 {scenario['name']}:")
        print("-" * 30)
        
        # Clear memory for each test
        conv_service.clear_memory()
        
        for i, question in enumerate(scenario['conversation'], 1):
            print(f"\nQ{i}: {question}")
            response = conv_service.ask_question(question)
            print(f"A{i}: {response['answer']}")
            
            # Check if AI understood the reference
            if i > 1:  # Follow-up questions
                understanding_check = "it" in question.lower() or "that" in question.lower() or "those" in question.lower() or "which" in question.lower()
                if understanding_check:
                    print(f"   💡 Follow-up reference detected: {'✅' if len(response['answer']) > 50 else '❌'}")

def test_memory_limits():
    """Test what happens with very long conversations"""
    print("\n\n⚠️  Testing Memory Limits")
    print("=" * 50)
    
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    # Test with buffer memory (unlimited)
    print("\n📈 Testing buffer memory with many questions...")
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    # Generate many questions
    questions = [
        "What's this person's name?",
        "What programming languages do they know?",
        "Tell me about Python experience",
        "What about JavaScript?",
        "Any Java experience?",
        "Tell me about their education",
        "What was their GPA?",
        "What's their first job?",
        "What about the second job?",
        "Current position details?",
        "What projects are mentioned?",
        "Any machine learning work?",
        "Web development experience?",
        "Database skills?",
        "Cloud experience?",
        "Leadership experience?",
        "Team size managed?",
        "Biggest achievement?",
        "Any certifications?",
        "Salary expectations?"  # This one should fail since not in resume
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\nQ{i}: {question}")
        try:
            response = conv_service.ask_question(question)
            summary = conv_service.get_memory_summary()
            print(f"A{i}: {response['answer'][:100]}...")
            print(f"    Memory: {summary['conversation_turns']} turns, ~{summary['estimated_tokens']} tokens")
            
            # Warn if memory getting large
            if summary['estimated_tokens'] > 3000:
                print("    ⚠️  Memory getting large!")
                
        except Exception as e:
            print(f"❌ Error at question {i}: {e}")
            break

def test_memory_switching():
    """Test switching between memory types mid-conversation"""
    print("\n\n🔄 Testing Memory Type Switching")
    print("=" * 50)
    
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    # Start conversation
    print("\n1️⃣ Starting with buffer memory...")
    conv_service.ask_question("What programming languages does this person know?")
    conv_service.ask_question("Tell me about their Python experience")
    
    print(f"Buffer memory: {conv_service.get_memory_summary()['conversation_turns']} turns")
    
    # Switch to window memory
    print("\n2️⃣ Switching to window memory...")
    conv_service.switch_memory_type("window")
    
    # Continue conversation (should lose previous context)
    response = conv_service.ask_question("What were we just discussing?")
    print(f"Response after memory switch: {response['answer'][:100]}...")
    
    # Add new conversation
    conv_service.ask_question("What's their work experience?")
    conv_service.ask_question("Which company was most recent?")
    
    print(f"Window memory: {conv_service.get_memory_summary()['conversation_turns']} turns")

def interactive_test():
    """Interactive test mode for manual testing"""
    print("\n\n💬 Interactive Test Mode")
    print("=" * 50)
    print("Commands:")
    print("  - Type questions normally")
    print("  - 'switch buffer/window/summary' to change memory type")
    print("  - 'clear' to clear memory")
    print("  - 'memory' to see memory summary")
    print("  - 'debug' to see detailed memory")
    print("  - 'quit' to exit")
    
    processor = ResumeProcessor()
    chunks = processor.load_resume("test_resume.txt")
    vector_service = VectorService()
    vector_store = vector_service.create_vector_store(chunks)
    
    conv_service = ConversationService(vector_store, memory_type="buffer")
    
    while True:
        try:
            user_input = input("\n💭 You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                conv_service.clear_memory()
                print("🧹 Memory cleared!")
            elif user_input.lower() == 'memory':
                summary = conv_service.get_memory_summary()
                print(f"📊 Memory Summary: {summary}")
            elif user_input.lower() == 'debug':
                conv_service.debug_memory()
            elif user_input.lower().startswith('switch '):
                memory_type = user_input.split(' ')[1]
                try:
                    conv_service.switch_memory_type(memory_type)
                except ValueError as e:
                    print(f"❌ Error: {e}")
            elif user_input:
                response = conv_service.ask_question(user_input)
                print(f"🤖 Assistant: {response['answer']}")
                
                # Show quick memory info
                summary = conv_service.get_memory_summary()
                print(f"    💭 Memory: {summary['conversation_turns']} turns ({summary['memory_type']})")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🚀 ResumeGPT Conversation Memory Test Suite")
    print("=" * 60)
    
    # Run automatic tests
    try:
        test_basic_conversation()
        test_memory_types()
        test_follow_up_understanding()
        test_memory_limits()
        test_memory_switching()
        
        print("\n\n✅ All automatic tests completed!")
        
        # Ask if user wants interactive mode
        while True:
            choice = input("\n🤔 Run interactive test mode? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                interactive_test()
                break
            elif choice in ['n', 'no']:
                print("👋 Tests completed!")
                break
            else:
                print("Please enter 'y' or 'n'")
                
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()