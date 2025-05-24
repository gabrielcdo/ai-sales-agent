from app.core.singleton import singleton

from opik.integrations.langchain import OpikTracer
import opik
import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# os.environ["OPIK_BASE_URL"] = 'http://opik-backend-1/api'
# os.environ["OPIK_URL_OVERRIDE"] = 'http://opik_default:5173/api'


@singleton
class Resources:
    def __init__(self):
        with open("/src/faiss_indexes/kb_texts.pkl", "rb") as f:
            self.documents = pickle.load(f)
        self.faiss_index = faiss.read_index("/src/faiss_indexes/kb_faiss.index")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.opik_client =opik.Opik()