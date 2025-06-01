# ingest.py
from utils.pdf_reader import extract_text_from_pdf
from utils.chunker import chunk_text
from utils.embedder import get_embedding
import faiss
import numpy as np

def ingest(pdf_path):
    print("📄 Reading PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Text length: {len(text)}")

    print("✂️ Chunking text...")
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        print("❌ No chunks found. PDF might be empty.")
        return

    print("🧠 Generating embeddings...")
    embeddings = [get_embedding(chunk) for chunk in chunks]

    print("💾 Saving to FAISS...")
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, "embeddings.index")
    np.save("texts.npy", np.array(chunks))

    print("✅ Done! Embeddings stored.")

if __name__ == "__main__":
    ingest("data/IPC.pdf")
