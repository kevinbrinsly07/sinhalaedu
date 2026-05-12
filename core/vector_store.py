"""Vector store implementation for RAG pipeline."""

import os
import uuid
from typing import List, Optional, Dict, Any
import numpy as np
from pathlib import Path

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

from config import settings
from core.embeddings import EmbeddingService


class VectorStore:
    """
    Vector store for storing and retrieving document embeddings.
    Uses FAISS for efficient similarity search.
    """

    def __init__(self, persist_dir: str = "./data/vectors"):
        """Initialize vector store."""
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.embedding_service = EmbeddingService()
        self.index = None
        self.metadata = {}
        self.index_path = self.persist_dir / "faiss.index"
        self.metadata_path = self.persist_dir / "metadata.json"
        
        if FAISS_AVAILABLE:
            self._load_or_create_index()

    def _load_or_create_index(self):
        """Load existing index or create new one."""
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self._load_metadata()
        else:
            # Create index with embedding dimension
            dim = 1536  # OpenAI embedding dimension
            self.index = faiss.IndexFlatL2(dim)

    def _load_metadata(self):
        """Load metadata from file."""
        import json
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)

    def _save_metadata(self):
        """Save metadata to file."""
        import json
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    async def add_material(self, file) -> str:
        """
        Add uploaded material to vector store.
        
        Args:
            file: Uploaded file (PDF, DOCX, TXT)
        
        Returns:
            material_id
        """
        material_id = str(uuid.uuid4())
        
        # Extract text from file
        content = await self._extract_text(file)
        
        # Store material info
        self.metadata[material_id] = {
            "id": material_id,
            "filename": file.filename,
            "content_length": len(content),
            "created_at": str(__import__('datetime').datetime.now()),
        }
        
        # Add chunks to vector store
        chunks = self._split_text(content)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{material_id}:chunk:{i}"
            await self.add_chunk(chunk_id, chunk)
        
        self._save_metadata()
        return material_id

    async def add_text_material(
        self,
        content: str,
        title: str,
        subject: str,
        grade: int,
    ) -> str:
        """Add text material directly."""
        material_id = str(uuid.uuid4())
        
        self.metadata[material_id] = {
            "id": material_id,
            "title": title,
            "subject": subject,
            "grade": grade,
            "content_length": len(content),
            "created_at": str(__import__('datetime').datetime.now()),
        }
        
        chunks = self._split_text(content)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{material_id}:chunk:{i}"
            await self.add_chunk(chunk_id, chunk)
        
        self._save_metadata()
        return material_id

    async def add_chunk(self, chunk_id: str, content: str):
        """Add a single chunk to vector store."""
        if not FAISS_AVAILABLE:
            return
        
        # Get embedding
        embedding = await self.embedding_service.embed(content)
        embedding = np.array([embedding]).astype('float32')
        
        # Add to index
        self.index.add(embedding)
        
        # Store metadata
        self.metadata[chunk_id] = {
            "id": chunk_id,
            "content": content,
            "created_at": str(__import__('datetime').datetime.now()),
        }
        
        self._save_index()
        self._save_metadata()

    def _save_index(self):
        """Save FAISS index to disk."""
        if FAISS_AVAILABLE and self.index:
            faiss.write_index(self.index, str(self.index_path))

    def _split_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into chunks."""
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i : i + chunk_size])
        
        return chunks

    async def _extract_text(self, file) -> str:
        """Extract text from uploaded file."""
        # Simple implementation - expand based on file type
        content = await file.read()
        return content.decode('utf-8', errors='ignore')

    async def search(
        self,
        query: str,
        subject: Optional[str] = None,
        grade: Optional[int] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Search for similar content."""
        if not FAISS_AVAILABLE:
            return []
        
        query_embedding = await self.embedding_service.embed(query)
        query_embedding = np.array([query_embedding]).astype('float32')
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            chunk_id = list(self.metadata.keys())[idx]
            chunk_info = self.metadata.get(chunk_id, {})
            results.append({
                "chunk_id": chunk_id,
                "content": chunk_info.get("content", ""),
                "score": float(distance),
                "subject": chunk_info.get("subject"),
                "grade": chunk_info.get("grade"),
            })
        
        return results

    async def list_materials(
        self,
        subject: Optional[str] = None,
        grade: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """List all materials."""
        materials = []
        for material_id, info in self.metadata.items():
            if ":" not in material_id:  # Only list main materials, not chunks
                if subject and info.get("subject") != subject:
                    continue
                if grade and info.get("grade") != grade:
                    continue
                materials.append(info)
        
        return materials

    async def delete_material(self, material_id: str):
        """Delete material from vector store."""
        # Remove all chunks for this material
        chunks_to_remove = [
            k for k in self.metadata.keys()
            if k.startswith(f"{material_id}:")
        ]
        
        for chunk_id in chunks_to_remove:
            del self.metadata[chunk_id]
        
        # Remove material itself
        if material_id in self.metadata:
            del self.metadata[material_id]
        
        self._save_metadata()
