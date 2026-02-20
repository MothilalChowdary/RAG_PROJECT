from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_loader import load_all_documents

class ChunkerEmbedder:

    def __init__(self,
                 model_name: str = "all-MiniLM-L6-v2",
                 max_chunk_size: int = 800,
                 chunk_overlap: int = 150

                 ):

        self.model = SentenceTransformer(model_name)
        self.chunk_overlap = chunk_overlap
        self.max_chunk_size = max_chunk_size

    def chunk(self, docs):

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=self.max_chunk_size,
        chunk_overlap=self.chunk_overlap,
        separators=[
            r"(?:^|\n)\d+(?:\.\d+)*\s",   # 1, 1.1, 1.1.2 (even at start of file)
            r"\nSection\s+\d+",      # Section 1
            r"\n[A-Z][A-Z\s]{3,}\n", # ALL CAPS headings
            "\n\n",
            "\n",
            " ",
            ""
        ],
        is_separator_regex=True)

        chunks = text_splitter.split_documents(docs)
        return chunks


    def embed_chunks(self, chunks):

        texts = [chunk.page_content for chunk in chunks]

        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
            )

        print(f"[INFO] Embeddings shape: {embeddings.shape}")

        return embeddings


if __name__ == "__main__":
    
    docs = load_all_documents("data")
    embed = ChunkerEmbedder()
    chunks = embed.chunk(docs)
    embeddings = embed.embed_chunks(chunks)
    print("[INFO] Example embedding:", embeddings[0] if len(embeddings) > 0 else None)