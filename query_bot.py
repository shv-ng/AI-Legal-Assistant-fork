import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Hugging Face API token for Mistral 
HF_API_TOKEN=os.getenv("API_TOKEN")  # Replace with your actual token or use os.getenv("HF
HF_MODEL_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load FAISS index and chunks
index = faiss.read_index("embeddings.index")
chunks = np.load("texts.npy", allow_pickle=True)

# ✅ Generate embedding for a query
def get_embedding(text):
    return model.encode(text)

# ✅ Search similar chunks
def search_chunks(query, top_k=3):
    query_emb = get_embedding(query)

    if index.ntotal == 0:
        return ["⚠️ FAISS index is empty! Run `ingest.py` first."]

    D, I = index.search(np.array([query_emb]).astype("float32"), top_k)
    return [chunks[i] for i in I[0] if 0 <= i < len(chunks)]

# ✅ Query Hugging Face Inference API
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
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return "⚠️ Unexpected response format from Hugging Face."
    elif response.status_code == 404:
        return "❌ Error: 404 - Model not found. Please check the model name or availability."
    elif response.status_code == 403:
        return "❌ Error: 403 - Access denied. Check if your token has inference access."
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# ✅ Main chat loop
if __name__ == "__main__":
    print("✅ Chatbot is running...")

    while True:
        question = input("Ask a legal question (or type 'exit' to quit): ").strip()
        if not question or question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        top_chunks = search_chunks(question)
        answer = generate_answer(top_chunks, question)
        print("\n🤖 Answer:\n", answer, "\n")
