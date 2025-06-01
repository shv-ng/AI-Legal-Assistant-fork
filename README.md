
# ⚖️ AI Legal Assistant Chatbot (GenAI + RAG)

This is a Python-based Legal Assistant chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer legal questions from the **Indian Penal Code (IPC)**.

It parses a legal PDF, chunks the text, embeds it into vectors using Hugging Face's `sentence-transformers`, stores it in a **FAISS** index, and uses a Hugging Face **LLM** (Zephyr 7B) to answer user queries.

## 🚀 Features

- 📄 Parses IPC legal PDF using PyMuPDF
- ✂️ Chunks long legal text into manageable pieces
- 🧠 Embeds chunks using `all-MiniLM-L6-v2` from Hugging Face
- 🔍 Searches relevant sections using FAISS
- 💬 Generates answers using HuggingFaceH4/zephyr-7b-beta
- ✅ Runs fully locally with only Hugging Face inference API

## 🧰 Tech Stack

| Component         | Library/Tool                     |
|------------------|----------------------------------|
| PDF Parsing      | `PyMuPDF` (fitz)                 |
| Text Chunking    | Custom Python function           |
| Embedding        | `sentence-transformers`          |
| Vector Search    | `faiss-cpu`                      |
| LLM              | `HuggingFaceH4/zephyr-7b-beta`   |
| Chat UI (optional) | `Streamlit` (not added yet)    |

## 📁 Folder Structure

```
AI Legal Assistant/
├── data/
│   └── IPC.pdf                     # Indian Penal Code PDF
├── utils/
│   ├── pdf_reader.py              # Extracts text from PDF
│   ├── chunker.py                 # Splits text into chunks
│   └── embedder.py                # Creates embeddings
├── embeddings.index               # FAISS vector index
├── texts.npy                      # Saved chunks
├── ingest.py                      # Run once to process PDF
├── query_bot.py                   # Ask questions here
├── requirements.txt
└── README.md
```

## ✅ How to Run

### 1. 📦 Install Requirements

```bash
pip install -r requirements.txt
```

### 2. 📄 Prepare IPC PDF

Place your IPC PDF in `data/IPC.pdf` (should be text-based, not scanned).

### 3. 🧠 Ingest PDF (Run once)

```bash
python ingest.py
```

### 4. 🤖 Start Chatbot

```bash
python query_bot.py
```

Then type:

```
Ask a legal question (or type 'exit' to quit): What is Section 302 of IPC?
```

## 🔐 Hugging Face API Token

Set your Hugging Face API token in `query_bot.py`:

```python
HF_API_TOKEN = "your_hf_token_here"
```

Get yours from: https://huggingface.co/settings/tokens

## 📦 requirements.txt

```txt
faiss-cpu
numpy
requests
sentence-transformers
pymupdf
```

## 🎓 Learning Resources

Full roadmap PDF with learning videos:  
📥 `AI_Legal_Assistant_Learning_Roadmap.pdf` (included in this repo)

## ✨ Credits

Built with ❤️ by Vaibhav  
LLM powered by Hugging Face `zephyr-7b-beta`.

## 🔜 What's Next?

- 💬 Build a Streamlit chat interface
- 🧠 Add source section highlighting
- 💾 Save Q&A history in a DB
- 🌐 Deploy online on Render/Streamlit Cloud
