from sentence_transformers import SentenceTransformer
import faiss
import pickle

# === CONFIG ===
KB_PATH = "faiss_indexes/sailer_knowledge_base.txt"
INDEX_OUTPUT = "faiss_indexes/kb_faiss.index"
TEXTS_OUTPUT = "faiss_indexes/kb_texts.pkl"
EMBEDDINGS_OUTPUT = "faiss_indexes/kb_embeddings.pkl"
CHUNK_SIZE = 512  # ajustável

# === 1. Carregar o texto da base ===
with open(KB_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()


# === 2. Quebrar o texto em chunks com overlapping ===
def split_text(text, max_length=CHUNK_SIZE, overlap=200):
    if not text.strip():
        return []
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += para + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())
            # Adiciona overlapping: pega os últimos 'overlap' caracteres do chunk atual, ignorando '\n\n' extras
            current_clean = current.replace("\n\n", "")
            if overlap > 0 and len(current_clean) > overlap:
                overlap_text = current_clean[-overlap:]
                # Garante que não haja '\n\n' entre overlap e para
                para_clean = para.lstrip("\n")
                current = overlap_text + para_clean + "\n\n"
            else:
                current = para + "\n\n"
    if current.strip():
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
query = "Achei caro o serviço de vocês. O que vocês podem fazer para me ajudar?"
query_embedding = model.encode([query])
D, I = index.search(query_embedding, k=3)  # k=3 retorna os 3 mais próximos

print("\nExemplo de consulta:")
print("Pergunta:", query)
for rank in range(3):
    print(f"\nTop {rank+1}:")
    print("Chunk mais similar:", documents[I[0][rank]])
    print("Distância:", D[0][rank])


# Chunk mais similar: ara sua operação?”

# 👤 Lead: “Achei meio caro o plano de vocês.”
# 🤖 Sailer AI: “Entendo. Muitas empresas começam pelo plano base e evoluem com ROI. Quer ver um exemplo de cliente com perfil parecido?”
#
# 👤 Lead: “Já uso outra ferramenta de automação.”
# 🤖 Sailer AI: “Ótimo! A Sailer pode trabalhar em conjunto com sua ferramenta atual, ampliando a cobertura de atendimento e aumentando conversões.”
#
# 📈 BENEFÍCIOS PARA SEU TIME COMERCIAL
# 0x mais conversões com mesma equipe
#
# 8% de redução em tempo operacional
