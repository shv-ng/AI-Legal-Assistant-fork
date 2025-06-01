import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embedding, text):
        self.index.add(np.array([embedding]).astype('float32'))
        self.texts.append(text)

    def save(self, index_path="embeddings.index", texts_path="texts.npy"):
        faiss.write_index(self.index, index_path)
        with open(texts_path, "wb") as f:
            np.save(f, self.texts)

    def load(self, index_path="embeddings.index", texts_path="texts.npy"):
        self.index = faiss.read_index(index_path)
        with open(texts_path, "rb") as f:
            self.texts = np.load(f, allow_pickle=True)
