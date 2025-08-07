from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from .vector_service import load_faiss_index
from .deepseek_service import get_deepseek_llm

try:
    from langchain_openai import OpenAI
    USE_OPENAI = True
except Exception:  # Fallback stub for environments without OpenAI access
    from langchain.llms.base import LLM
    USE_OPENAI = False

    class OpenAI(LLM):
        @property
        def _llm_type(self) -> str:  # type: ignore[override]
            return "stub"

        def _call(self, prompt: str, stop=None) -> str:  # type: ignore[override]
            return prompt


COVER_LETTER_PROMPT = PromptTemplate.from_template(
    "You are a career coach. Given my résumé and this job description:\n{job_desc}\nGenerate a concise cover letter."
)

INTERVIEW_PROMPT = PromptTemplate.from_template(
    "You are an interviewer. Based on my résumé, simulate 5 interview questions for a {role} role."
)


def get_llm():
    """Get the appropriate LLM instance (DeepSeek preferred, OpenAI fallback)"""
    try:
        return get_deepseek_llm()
    except Exception as e:
        print(f"⚠️  DeepSeek not available ({e}), falling back to OpenAI")
        return OpenAI()


def answer_query(question: str):
    import os
    # Ensure we're using the correct path
    index_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vector_store", "faiss_index")
    index_path = os.path.abspath(index_path)
    
    store = load_faiss_index(index_path)
    qa = RetrievalQA.from_chain_type(
        llm=get_llm(), chain_type="stuff", retriever=store.as_retriever()
    )
    return qa.run(question)


def gen_cover_letter(job_desc: str):
    chain = LLMChain(llm=get_llm(), prompt=COVER_LETTER_PROMPT)
    return chain.run(job_desc)


def gen_interview_questions(role: str):
    chain = LLMChain(llm=get_llm(), prompt=INTERVIEW_PROMPT)
    return chain.run(role)
