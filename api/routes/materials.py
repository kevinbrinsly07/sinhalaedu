"""Routes for managing educational materials."""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from schemas.material import MaterialResponse, MaterialUploadRequest
from core.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore()


@router.post("/upload")
async def upload_material(file: UploadFile = File(...)):
    """
    Upload educational material for RAG pipeline.
    
    Supported formats: PDF, TXT, DOCX
    """
    try:
        material_id = await vector_store.add_material(file)
        return {
            "material_id": material_id,
            "filename": file.filename,
            "status": "uploaded",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading material: {str(e)}")


@router.post("/add-text")
async def add_text_material(request: MaterialUploadRequest):
    """
    Add text material directly to the vector store.
    
    Useful for adding Sinhala curriculum content.
    """
    try:
        material_id = await vector_store.add_text_material(
            content=request.content,
            title=request.title,
            subject=request.subject,
            grade=request.grade,
        )
        return {
            "material_id": material_id,
            "title": request.title,
            "status": "added",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search")
async def search_materials(
    query: str,
    subject: str = None,
    grade: int = None,
    top_k: int = 5,
):
    """Search materials using semantic search."""
    try:
        results = await vector_store.search(
            query=query,
            subject=subject,
            grade=grade,
            top_k=top_k,
        )
        return {
            "query": query,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/materials")
async def list_materials(subject: str = None, grade: int = None):
    """List all materials in vector store."""
    try:
        materials = await vector_store.list_materials(subject=subject, grade=grade)
        return {
            "count": len(materials),
            "materials": materials,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/materials/{material_id}")
async def delete_material(material_id: str):
    """Delete material from vector store."""
    try:
        await vector_store.delete_material(material_id)
        return {"status": "deleted", "material_id": material_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
