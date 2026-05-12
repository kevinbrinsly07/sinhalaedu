"""Schemas for exam papers."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class QuestionType(str, Enum):
    """Types of questions."""
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    TRUE_FALSE = "true_false"


class QuestionResponse(BaseModel):
    """A single exam question."""
    id: str
    question_text: str = Field(..., description="Question in Sinhala")
    question_type: QuestionType
    marks: int = Field(default=1, ge=1)
    options: Optional[List[str]] = Field(None, description="Options for multiple choice")
    correct_answer: Optional[str] = Field(None, description="Correct answer (for validation)")
    explanation: Optional[str] = Field(None, description="Explanation for the answer")


class PaperResponse(BaseModel):
    """Generated exam paper."""
    paper_id: str
    title: str = Field(..., description="Paper title in Sinhala")
    subject: str
    grade: int
    total_marks: int
    duration_minutes: int = Field(default=120)
    questions: List[QuestionResponse]
    instructions: str = Field(default="", description="Exam instructions in Sinhala")
    generated_at: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GeneratePaperRequest(BaseModel):
    """Request to generate an exam paper."""
    subject: str = Field(..., description="Subject name (e.g., Mathematics, Science)")
    grade: int = Field(..., ge=1, le=13, description="Grade level")
    num_questions: int = Field(default=10, ge=5, le=50)
    total_marks: int = Field(default=100, ge=50, le=500)
    question_types: Optional[List[QuestionType]] = Field(
        default=None,
        description="Allowed question types. If None, mix of all types."
    )
    difficulty_level: str = Field(
        default="mixed",
        description="Difficulty: easy, medium, hard, or mixed"
    )
    include_explanation: bool = Field(
        default=True,
        description="Include explanations for answers"
    )
    language: str = Field(default="sinhala")
    custom_content: Optional[str] = Field(
        None,
        description="Custom curriculum content to base questions on"
    )


class PaperListResponse(BaseModel):
    """List of generated papers."""
    count: int
    papers: List[PaperResponse]
