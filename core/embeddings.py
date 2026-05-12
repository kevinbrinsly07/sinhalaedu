"""Embedding service for converting text to vectors."""

from openai import AsyncOpenAI
from config import settings


class EmbeddingService:
    """Generate embeddings using OpenAI."""

    def __init__(self):
        """Initialize embedding service."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    async def embed(self, text: str) -> list:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model,
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")

    async def embed_batch(self, texts: list) -> list:
        """Generate embeddings for multiple texts."""
        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self.model,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise Exception(f"Error generating batch embeddings: {str(e)}")
