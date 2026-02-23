from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from dotenv import load_dotenv
import os
import uuid


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API = os.getenv("QDRANT_API")


class QdrantVectorDB:
    def __init__(
        self,
        collection_name,
        url=QDRANT_URL,
        api_key=QDRANT_API,
        vector_size=384,
        distance=Distance.COSINE
    ):

        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance

        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )
        self._create_collection()

    def _create_collection(self):
        collections = self.client.get_collections().collections
        existing = [col.name for col in collections]

        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=self.distance
                ),
            )
            print(f"Collection '{self.collection_name}' created.")

    def insert_records(self, records):

        points = []

        for record in records:
            payload = record["metadata"].copy()
            payload["text"] = record["text"]

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=record["embedding"],
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"{len(points)} records inserted successfully.")

