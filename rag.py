import os
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API = os.getenv("QDRANT_API")
COLLECTION_NAME = "documents"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API,
)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

llm_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def embed_query(query: str):
    return embedding_model.encode(query).tolist()


def search_qdrant(query: str, user_role: str, top_k: int = 3):

    query_vector = embed_query(query)

    search_result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="access_roles",
                    match=MatchAny(any=[user_role])
                )
            ]
        ),
        limit=top_k,
    )
    retrieved_docs = [hit.payload.get("text", "") for hit in search_result.points]
    source = [hit.payload.get("source", "") for hit in search_result.points]
    return retrieved_docs, source

def build_messages(query: str, retrieved_docs: list[str], chat_history: list[dict]):
    context = "\n\n".join(retrieved_docs)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict Company Retrieval Augmented Generation (RAG) assistant.\n"
                "Use the provided context AND the previous chat history to answer the question.\n"
                "If the answer is present in the context, explain it clearly in a well-written paragraph.\n"
                "Do not simply list items — explain them naturally.\n"
                "If the answer is NOT present in the context, respond with exactly:\n"
                "I don't know.\n"
                "Stay conversational and helpful while adhering to the context."
            )
        }
    ]
    
    # Add chat history
    messages.extend(chat_history)
    
    # Add new user query with context
    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}"
    })
    
    return messages

def generate_answer(messages: list[dict]):

    response = llm_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.4,
    )

    return response.choices[0].message.content

def rag_pipeline(query: str, user_role: str, chat_history: list[dict]):
    retrieved_docs, source = search_qdrant(query, user_role)
    messages = build_messages(query, retrieved_docs, chat_history)
    answer = generate_answer(messages)
    return answer, list(set(source))

