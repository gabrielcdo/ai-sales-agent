from sentence_transformers import SentenceTransformer
import faiss
import pickle

# === CONFIG ===
KB_PATH = "faiss_indexes/solarbright_knowledge_base.txt"
INDEX_OUTPUT = "faiss_indexes/kb_faiss.index"
TEXTS_OUTPUT = "faiss_indexes/kb_texts.pkl"
EMBEDDINGS_OUTPUT = "faiss_indexes/kb_embeddings.pkl"
CHUNK_SIZE = 1024  # ajustável

# === 1. Carregar o texto da base ===
with open(KB_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()


# === 2. Quebrar o texto em chunks com overlapping ===
def split_text(text, max_length=CHUNK_SIZE, overlap=200):
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += para + "\n\n"
        else:
            chunks.append(current.strip())
            # Adiciona overlapping: pega os últimos 'overlap' caracteres do chunk atual
            if overlap > 0 and len(current) > overlap:
                current = current[-overlap:] + para + "\n\n"
            else:
                current = para + "\n\n"
    if current:
        chunks.append(current.strip())
    return chunks

documents = split_text(raw_text, max_length=CHUNK_SIZE, overlap=200)

# === 3. Gerar embeddings ===
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")  # ou outro modelo local
embeddings = model.encode(documents, show_progress_bar=True)

# === 4. Criar índice FAISS ===
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === 5. Salvar ===
faiss.write_index(index, INDEX_OUTPUT)
with open(TEXTS_OUTPUT, "wb") as f:
    pickle.dump(documents, f)
with open(EMBEDDINGS_OUTPUT, "wb") as f:
    pickle.dump(embeddings, f)

print(f"✅ Index criado com {len(documents)} chunks.")

# === Exemplo de consulta ao índice ===
# Consulta de exemplo: buscar os 3 chunks mais similares a uma pergunta
query = "Qual preço se eu for comprar aqui pra minha casa? "
query_embedding = model.encode([query])
D, I = index.search(query_embedding, k=3)  # k=3 retorna os 3 mais próximos

print("\nExemplo de consulta:")
print("Pergunta:", query)
for rank in range(3):
    print(f"\nTop {rank+1}:")
    print("Chunk mais similar:", documents[I[0][rank]])
    print("Distância:", D[0][rank])