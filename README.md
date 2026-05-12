# Sinhala Exam Paper Generator

A FastAPI-based system for generating Sinhala mock exam papers for students and teachers using RAG (Retrieval-Augmented Generation) pipeline powered by OpenAI.

## Features

- 📝 **Automatic Exam Paper Generation** - Generate contextual Sinhala exam papers
- 🔍 **RAG Pipeline** - Retrieves relevant material from knowledge base before generating questions
- 📚 **Material Management** - Upload and manage educational materials (PDF, DOCX, TXT)
- 🤖 **AI-Powered** - Uses OpenAI GPT-4 for intelligent question generation
- 🎯 **Multiple Question Types** - Multiple choice, short answer, essay, true/false
- 📊 **Grade-Based Generation** - Customize papers by grade level
- 🌍 **Sinhala Language Support** - Full Sinhala text support throughout

## Prerequisites

- Python 3.8+
- OpenAI API key
- PostgreSQL (optional, for production)
- Redis (optional, for caching)

## Installation

1. **Clone repository and navigate to directory:**
```bash
cd /Users/kevinbrinsly/sinhalaedu
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

Edit `.env` file with your settings:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
APP_ENV=development
DEBUG=True
```

## Running the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Generate Exam Paper
```bash
POST /api/v1/papers/generate
Content-Type: application/json

{
  "subject": "Mathematics",
  "grade": 10,
  "num_questions": 10,
  "total_marks": 100,
  "difficulty_level": "mixed",
  "language": "sinhala"
}
```

#### Upload Learning Material
```bash
POST /api/v1/materials/upload
Content-Type: multipart/form-data

[file content]
```

#### Add Text Material
```bash
POST /api/v1/materials/add-text
Content-Type: application/json

{
  "title": "Chapter Title",
  "content": "Material content...",
  "subject": "Mathematics",
  "grade": 10
}
```

#### Search Materials
```bash
GET /api/v1/materials/search?query=algebra&subject=Mathematics&grade=10
```

#### Submit Exam
```bash
POST /api/v1/exams/submit
Content-Type: application/json

{
  "exam_id": "exam_uuid",
  "student_id": "student_uuid",
  "answers": [
    {
      "question_id": "q_uuid",
      "answer": "answer text"
    }
  ]
}
```

## Project Structure

```
sinhalaedu/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
│
├── api/
│   └── routes/
│       ├── papers.py      # Paper generation endpoints
│       ├── materials.py   # Material management endpoints
│       └── exams.py       # Exam submission endpoints
│
├── schemas/
│   ├── paper.py           # Paper/question schemas
│   ├── material.py        # Material schemas
│   └── exam.py            # Exam schemas
│
├── core/
│   ├── rag_pipeline.py    # RAG pipeline implementation
│   ├── vector_store.py    # Vector store (FAISS)
│   └── embeddings.py      # Embedding service
│
└── data/
    └── vectors/           # Vector store persistence
```

## RAG Pipeline Workflow

1. **Material Upload** → Store documents in vector store
2. **Query Processing** → User requests exam paper
3. **Retrieval** → Search vector store for relevant material
4. **Context Preparation** → Prepare context from retrieved docs
5. **Generation** → Use OpenAI to generate questions based on context
6. **Paper Creation** → Compile final exam paper

## Development

### Adding New Question Types

Edit `schemas/paper.py` and add to `QuestionType` enum:

```python
class QuestionType(str, Enum):
    FILL_BLANK = "fill_blank"
```

### Customizing Prompt

Modify `_create_prompt()` in `core/rag_pipeline.py` to change question generation behavior.

### Database Integration

To enable database persistence, update `config.py` with:
```python
DATABASE_URL = "postgresql://user:password@localhost/sinhala_edu"
```

## TODO

- [ ] Database models and persistence
- [ ] Student progress tracking
- [ ] Teacher analytics dashboard
- [ ] Advanced PDF export
- [ ] Multi-language support
- [ ] Authentication & authorization
- [ ] Rate limiting
- [ ] Question bank management
- [ ] Answer key generation
- [ ] Performance analytics

## API Response Examples

### Generate Paper Response
```json
{
  "paper_id": "uuid",
  "title": "Mathematics Exam - Grade 10",
  "subject": "Mathematics",
  "grade": 10,
  "total_marks": 100,
  "duration_minutes": 120,
  "questions": [
    {
      "id": "uuid",
      "question_text": "පළමු සංඛ්‍යා කුමක්ද?",
      "question_type": "multiple_choice",
      "marks": 5,
      "options": ["1, 2, 3, 4", "2, 3, 5, 7", "1, 4, 6, 8"],
      "correct_answer": "2, 3, 5, 7",
      "explanation": "පළමු සංඛ්‍යා යනු..."
    }
  ],
  "instructions": "පරීක්ෂණ උපදෙස්...",
  "generated_at": "2026-05-12T10:30:00"
}
```

## Troubleshooting

### OpenAI API Key Error
- Ensure `.env` file has valid `OPENAI_API_KEY`
- Check API key has sufficient credits

### FAISS Import Error
Install with CPU version: `pip install faiss-cpu`

### Sinhala Text Display Issues
- Ensure UTF-8 encoding: `export PYTHONIOENCODING=utf-8`
- Check terminal supports Sinhala characters

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
