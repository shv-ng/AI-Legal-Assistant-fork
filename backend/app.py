# backend/app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Init FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("embeddings.index")
chunks = np.load("texts.npy", allow_pickle=True)

# Hugging Face API details
HF_API_TOKEN = os.getenv("API_TOKEN")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# Pydantic model for input
class QuestionRequest(BaseModel):
    question: str

# Helper to get embedding
def get_embedding(text):
    return model.encode(text)

# Search similar text chunks
def search_chunks(query, top_k=3):
    if index.ntotal == 0:
        return ["⚠️ FAISS index is empty. Please run ingest.py first."]
    query_emb = get_embedding(query)
    D, I = index.search(np.array([query_emb]).astype("float32"), top_k)
    return [chunks[i] for i in I[0] if 0 <= i < len(chunks)]

# Generate answer using HF model
def generate_answer(context_chunks, question):
    if "⚠️" in context_chunks[0]:
        return context_chunks[0]

    context_text = "\n\n".join(context_chunks)
    prompt = f"""You are a legal assistant. Based on the following Indian Penal Code context, answer the question clearly and simply.

Context:
{context_text}

Question: {question}
Answer:"""

    response = requests.post(
        url=HF_MODEL_URL,
        headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
        json={"inputs": prompt}
    )

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict):
            return result.get("generated_text", "⚠️ Unexpected response format.")
        else:
            return "⚠️ Unexpected format from Hugging Face API."
    elif response.status_code == 403:
        return "❌ 403 Forbidden - Invalid or unauthorized API token."
    elif response.status_code == 404:
        return "❌ 404 Not Found - Model may be unavailable or misspelled."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# POST endpoint to handle legal queries
@app.post("/ask")
def ask_question(data: QuestionRequest):
    chunks_found = search_chunks(data.question)
    answer = generate_answer(chunks_found, data.question)
    return {"question": data.question, "answer": answer, "context": chunks_found}

# GET route for testing server is running
@app.get("/")
def root():
    return {"message": "✅ AI Legal Assistant backend is running."}

# Optional: Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "faiss_index_loaded": index.ntotal > 0}
