"""Schemas for exam submission and results."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class StudentAnswer(BaseModel):
    """Student's answer to a question."""
    question_id: str
    answer: str
    time_spent_seconds: Optional[int] = None


class SubmitExamRequest(BaseModel):
    """Submit exam for evaluation."""
    exam_id: str
    student_id: str
    answers: List[StudentAnswer]
    total_time_seconds: Optional[int] = None


class ExamResultResponse(BaseModel):
    """Exam evaluation result."""
    exam_id: str
    student_id: str
    total_questions: int
    correct_answers: int
    score: float
    percentage: float
    grade: Optional[str] = None
    feedback: Optional[str] = None
    detailed_results: Optional[List[Dict[str, Any]]] = None
    status: str
