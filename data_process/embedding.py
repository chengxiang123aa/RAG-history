from web.configs import EMBED_MODEL
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(EMBED_MODEL)

def get_embedding(content):
    embeddings = model.encode(content)
    return embeddings

  


