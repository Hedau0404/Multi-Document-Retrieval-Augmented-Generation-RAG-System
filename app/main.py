from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "service": "RAG-Engine"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)) -> dict:
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        reader = PdfReader(file.file)
        text = "".join(page.extract_text() or "" for page in reader.pages)

        logging.info(f"Extracted first 500 chars: {text[:500]}")

        return {
            "filename": file.filename,
            "character_count": len(text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/query")
async def query_rag(question: str) -> dict:
    return {
        "query": question,
        "answer": "Vector search not yet implemented."
    }