from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from .vector_service import load_faiss_index

try:
    from langchain_openai import OpenAI
except Exception:  # Fallback stub for environments without OpenAI access
    from langchain.llms.base import LLM

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


def answer_query(question: str):
    store = load_faiss_index("data/vector_store/faiss_index")
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=store.as_retriever()
    )
    return qa.run(question)


def gen_cover_letter(job_desc: str):
    chain = LLMChain(llm=OpenAI(), prompt=COVER_LETTER_PROMPT)
    return chain.run(job_desc)


def gen_interview_questions(role: str):
    chain = LLMChain(llm=OpenAI(), prompt=INTERVIEW_PROMPT)
    return chain.run(role)
