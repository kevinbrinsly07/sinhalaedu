"""Schemas for educational materials."""

from typing import Optional
from pydantic import BaseModel, Field


class MaterialUploadRequest(BaseModel):
    """Request to add text material."""
    title: str
    content: str
    subject: str
    grade: int
    metadata: Optional[dict] = Field(default_factory=dict)


class MaterialResponse(BaseModel):
    """Material information."""
    material_id: str
    title: str
    subject: str
    grade: int
    content_length: int
    chunk_count: int
    created_at: str
    updated_at: str


class SearchResult(BaseModel):
    """Search result for material."""
    chunk_id: str
    material_id: str
    title: str
    content: str
    score: float
    subject: str
    grade: int
