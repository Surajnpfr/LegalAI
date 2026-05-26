# app/db/init_qdrant.py
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv

load_dotenv()

def init_vector_db():
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=qdrant_url)
    collection_name = "nepali_laws"
    
    # Llama 3.2:3b native embedding output size is 3072 dims
    vector_size = 3072 

    collections = client.get_collections().collections
    if not any(c.name == collection_name for c in collections):
        print(f"Creating collection: {collection_name}...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        print("Collection created successfully!")
    else:
        print(f"Collection '{collection_name}' already exists.")

if __name__ == "__main__":
    init_vector_db()