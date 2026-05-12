"""Routes for managing exam papers."""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel
from core.rag_pipeline import RAGPipeline
from schemas.paper import (
    GeneratePaperRequest,
    PaperResponse,
    QuestionResponse,
)

router = APIRouter()

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()


class SubjectRequest(BaseModel):
    """Request model for listing subjects."""
    language: str = "sinhala"


@router.post("/generate", response_model=PaperResponse)
async def generate_exam_paper(request: GeneratePaperRequest) -> PaperResponse:
    """
    Generate a Sinhala exam paper.
    
    Args:
        request: Paper generation request with subject, grade, num_questions, etc.
    
    Returns:
        Generated exam paper with questions
    """
    try:
        paper = await rag_pipeline.generate_paper(request)
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating paper: {str(e)}")


@router.post("/generate-batch")
async def generate_batch_papers(
    subject: str,
    grade: int,
    num_papers: int = Query(1, ge=1, le=10),
    num_questions: int = Query(10, ge=5, le=50),
):
    """Generate multiple exam papers."""
    try:
        papers = await rag_pipeline.generate_batch_papers(
            subject=subject,
            grade=grade,
            num_papers=num_papers,
            num_questions=num_questions,
        )
        return {
            "count": len(papers),
            "papers": papers,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating papers: {str(e)}")


@router.get("/preview/{paper_id}")
async def preview_paper(paper_id: str):
    """Preview an exam paper."""
    try:
        paper = await rag_pipeline.get_paper(paper_id)
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subjects")
async def list_subjects(language: str = Query("sinhala")):
    """List available subjects for exam paper generation."""
    subjects = [
        "Mathematics",
        "Science",
        "History",
        "Geography",
        "Literature",
        "English",
        "Sinhala",
    ]
    return {"subjects": subjects, "language": language}
