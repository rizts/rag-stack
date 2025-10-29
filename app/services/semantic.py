import google.generativeai as genai
from app.utils.chunking import chunk_text
from app.services.embeddings_huggingface import HuggingFaceEmbeddingService
from app.services.vectorstore_qdrant import QdrantClientWrapper
from app.core.config import settings


class SemanticSearchService:
    """
    End-to-end RAG (Retrieval-Augmented Generation) pipeline:
    1. Chunk & embed documents
    2. Store embeddings to Qdrant
    3. Retrieve relevant context
    4. Generate final answer with Gemini LLM
    """

    def __init__(self):
        self.collection_name = "documents"
        self.embeddings = HuggingFaceEmbeddingService()
        self.qdrant = QdrantClientWrapper(collection_name=self.collection_name, vector_size=384)  # HuggingFace embeddings are 384-dim
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.llm = genai.GenerativeModel("gemini-1.0-pro")

    def index_text(self, text: str, metadata: dict | None = None):
        """
        Chunk a large document, embed each chunk using Gemini, and store in Qdrant.
        """
        chunks = chunk_text(text)
        vectors = self.embeddings.embed_texts(chunks)
        payloads = [{"content": c, **(metadata or {})} for c in chunks]
        self.qdrant.upsert_vectors(self.collection_name, vectors, payloads)
        return {"chunks_indexed": len(chunks)}

    def search(self, query: str, top_k: int = 3):
        """
        Retrieve the most relevant chunks from Qdrant using semantic similarity.
        """
        query_vector = self.embeddings.embed_text(query)
        results = self.qdrant.search_vectors(self.collection_name, query_vector, top_k=top_k)

        return [
            {"score": r.score, "content": r.payload.get("content", "")}
            for r in results
        ]

    def generate_answer(self, query: str, top_k: int = 3):
        """
        Combine retrieval and generation:
        1. Retrieve top-k similar chunks
        2. Compose a prompt with context
        3. Ask Gemini to generate a context-aware answer
        """
        retrieved_docs = self.search(query, top_k)
        if not retrieved_docs:
            return {"answer": "No relevant information found."}

        # Combine top-k chunks into one context string
        context = "\n\n".join([doc["content"] for doc in retrieved_docs])

        # Build a clear, concise system prompt
        prompt = f"""
        You are a helpful assistant. 
        Use the following context to answer the user's question accurately and clearly.

        Context:
        {context}

        Question: {query}
        """

        response = self.llm.generate_content(prompt)
        return {
            "query": query,
            "answer": response.text.strip(),
            "context_used": [doc["content"] for doc in retrieved_docs],
        }
