from data_loader import load_all_documents
from chunk import ChunkerEmbedder
from vector import QdrantVectorDB

if __name__ == "__main__":
    documnets = load_all_documents("data")
    chunker = ChunkerEmbedder()
    chunks = chunker.chunk(documnets)
    records = chunker.embed_chunks(chunks)
    vector_db = QdrantVectorDB("documents")
    vector_db.insert_records(records)