from app.core.singleton import singleton

import opik
import json
from sentence_transformers import SentenceTransformer
import faiss
import pickle


@singleton
class Resources:
    def __init__(self):
        with open("/src/faiss_indexes/kb_texts.pkl", "rb") as f:
            self.documents = pickle.load(f)
        self.faiss_index = faiss.read_index("/src/faiss_indexes/kb_faiss.index")
        self.sentence_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
        with open("/src/faiss_indexes/knowledge_base.json", "r") as f:
            self.knowledge_base = json.load(f)
        # Load prospect details from JSON
        with open("/src/faiss_indexes/prospects.json", "r") as f:
            self.prospects = json.load(f)
        self.opik_client = opik.Opik()
