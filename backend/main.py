from fastapi import FastAPI, File, UploadFile
from services.resume_service import load_resume
from services.vector_service import build_faiss_index
from services.generation_service import answer_query, gen_cover_letter, gen_interview_questions

app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"data/uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    docs = load_resume(path)
    build_faiss_index(docs)
    return {"status": "indexed"}


@app.get("/ask")
def ask(q: str):
    return {"answer": answer_query(q)}


@app.get("/cover-letter")
def cover(job_desc: str):
    return {"cover_letter": gen_cover_letter(job_desc)}


@app.get("/interview")
def interview(role: str):
    return {"questions": gen_interview_questions(role)}
