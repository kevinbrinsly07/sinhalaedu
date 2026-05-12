"""RAG (Retrieval-Augmented Generation) pipeline for exam paper generation."""

import uuid
from datetime import datetime
from typing import Optional
from openai import AsyncOpenAI

from config import settings
from core.vector_store import VectorStore
from schemas.paper import (
    GeneratePaperRequest,
    PaperResponse,
    QuestionResponse,
    QuestionType,
)


class RAGPipeline:
    """
    RAG pipeline for generating Sinhala exam papers.
    
    Retrieves relevant material from vector store and uses
    OpenAI to generate contextual questions.
    """

    def __init__(self):
        """Initialize RAG pipeline."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.vector_store = VectorStore()
        self.papers_store = {}  # In-memory storage for demo

    async def generate_paper(self, request: GeneratePaperRequest) -> PaperResponse:
        """
        Generate an exam paper using RAG.
        
        Process:
        1. Retrieve relevant material from vector store
        2. Generate questions based on retrieved content
        3. Create structured paper response
        """
        paper_id = str(uuid.uuid4())
        
        # Step 1: Retrieve relevant material
        retrieval_query = f"{request.subject} grade {request.grade} exam questions"
        retrieved_docs = await self.vector_store.search(
            query=retrieval_query,
            subject=request.subject,
            grade=request.grade,
            top_k=settings.TOP_K_RETRIEVAL,
        )

        # Prepare context from retrieved documents
        context = self._prepare_context(retrieved_docs)
        
        # Step 2: Generate questions
        questions = await self._generate_questions(
            request=request,
            context=context,
        )
        
        # Step 3: Create paper response
        total_marks = sum(q.marks for q in questions)
        
        paper = PaperResponse(
            paper_id=paper_id,
            title=f"{request.subject} Exam - Grade {request.grade}",
            subject=request.subject,
            grade=request.grade,
            total_marks=total_marks,
            duration_minutes=120,
            questions=questions,
            instructions="පරීක්ෂණ උපදෙස්:\n1. සියලු ප්‍රශ්නවලට පිළිතුරු දෙන්න.\n2. වැඩිපුරම ලකුණු ගණනය සඳහා පිටත ගණනය කිරීම් අවශ්ය නම් පෙන්නුවා දෙන්න.",
            generated_at=datetime.now().isoformat(),
        )
        
        # Store paper
        self.papers_store[paper_id] = paper
        
        return paper

    async def _generate_questions(
        self,
        request: GeneratePaperRequest,
        context: str,
    ) -> list:
        """Generate questions using OpenAI."""
        question_types = request.question_types or [
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.SHORT_ANSWER,
            QuestionType.ESSAY,
        ]
        
        prompt = self._create_prompt(
            subject=request.subject,
            grade=request.grade,
            num_questions=request.num_questions,
            question_types=[qt.value for qt in question_types],
            difficulty=request.difficulty_level,
            context=context,
        )
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Sinhala educator creating exam questions. Always respond in Sinhala language. Generate questions in JSON format.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=4000,
            )
            
            # Parse response and create question objects
            questions = await self._parse_questions(response.choices[0].message.content)
            return questions
            
        except Exception as e:
            raise Exception(f"Error generating questions: {str(e)}")

    def _create_prompt(
        self,
        subject: str,
        grade: int,
        num_questions: int,
        question_types: list,
        difficulty: str,
        context: str,
    ) -> str:
        """Create prompt for question generation."""
        return f"""
        ඉහත ශිෂ්‍යවරුන්ට විභාගය සඳහා {num_questions} ප්‍රශ්න සාදන්න.
        
        විෂය: {subject}
        ශ්‍රේණිය: {grade}
        난이도: {difficulty}
        ප්‍රශ්න වර්ගයන්: {', '.join(question_types)}
        
        පසුබිම තොරතුරු:
        {context}
        
        JSON ස්වරූපයෙන් පිළිතුරු දෙන්න:
        {{
            "questions": [
                {{
                    "question_text": "ප්‍රශ්නය සිංහලින්",
                    "type": "multiple_choice|short_answer|essay",
                    "marks": අගය,
                    "options": ["විකල්පය 1", "විකල්පය 2", ...] (සම්පූර්ණ ප්‍රශ්නයටපමණි),
                    "correct_answer": "සරිලි පිළිතුර",
                    "explanation": "පැහැදිලි කිරීම"
                }}
            ]
        }}
        """

    async def _parse_questions(self, response_text: str) -> list:
        """Parse questions from LLM response."""
        import json
        
        questions = []
        
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                data = json.loads(json_str)
                
                for q in data.get("questions", []):
                    question_id = str(uuid.uuid4())
                    
                    question = QuestionResponse(
                        id=question_id,
                        question_text=q.get("question_text", ""),
                        question_type=QuestionType(q.get("type", "short_answer")),
                        marks=q.get("marks", 1),
                        options=q.get("options"),
                        correct_answer=q.get("correct_answer"),
                        explanation=q.get("explanation"),
                    )
                    questions.append(question)
            
        except json.JSONDecodeError:
            # Fallback: create dummy questions
            pass
        
        return questions

    def _prepare_context(self, retrieved_docs: list) -> str:
        """Prepare context from retrieved documents."""
        context_parts = []
        
        for doc in retrieved_docs:
            content = doc.get("content", "")[:500]  # Limit content length
            context_parts.append(content)
        
        return "\n\n".join(context_parts)

    async def get_paper(self, paper_id: str) -> Optional[PaperResponse]:
        """Retrieve a generated paper."""
        return self.papers_store.get(paper_id)

    async def generate_batch_papers(
        self,
        subject: str,
        grade: int,
        num_papers: int,
        num_questions: int,
    ) -> list:
        """Generate multiple papers."""
        papers = []
        
        for _ in range(num_papers):
            request = GeneratePaperRequest(
                subject=subject,
                grade=grade,
                num_questions=num_questions,
            )
            paper = await self.generate_paper(request)
            papers.append(paper)
        
        return papers
