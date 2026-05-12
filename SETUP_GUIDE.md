"""
INSTALLATION AND SETUP GUIDE
Sinhala Exam Paper Generator
"""

# ============================================================================
# SYSTEM REQUIREMENTS
# ============================================================================

# - Python 3.8 or higher
# - pip (Python package manager)
# - OpenAI API key (from https://platform.openai.com/api-keys)
# - Optional: Docker & Docker Compose (for containerized deployment)
# - Optional: PostgreSQL 12+ (for production database)
# - Optional: Redis (for caching and sessions)


# ============================================================================
# INSTALLATION STEPS
# ============================================================================

"""
STEP 1: Clone or Extract Project
=================================
cd /Users/kevinbrinsly/sinhalaedu


STEP 2: Create Virtual Environment
===================================
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows


STEP 3: Install Dependencies
=============================
pip install -r requirements.txt

# If you want to use GPU for faster embeddings:
# pip install faiss-gpu  # Instead of faiss-cpu


STEP 4: Configure Environment Variables
========================================
cp .env.example .env

# Edit .env and add:
# - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys
# - OPENAI_MODEL: gpt-4 (or gpt-3.5-turbo)
# - APP_ENV: development or production
# - DATABASE_URL: (optional, for PostgreSQL)

Example .env:
"""
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4
APP_ENV=development
DEBUG=True
"""


STEP 5: Initialize Data Directories
=====================================
mkdir -p data/vectors logs


STEP 6: Run the Application
============================
# Development mode:
python main.py

# Production mode with multiple workers:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4


STEP 7: Access the Application
===============================
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
"""


# ============================================================================
# DOCKER DEPLOYMENT (OPTIONAL)
# ============================================================================

"""
Using Docker Compose to run everything:

STEP 1: Build and Start Services
=================================
docker-compose up -d

This starts:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- PgAdmin UI (port 5050)


STEP 2: View Logs
=================
docker-compose logs -f app


STEP 3: Stop Services
=====================
docker-compose down


STEP 4: Rebuild after code changes
===================================
docker-compose up -d --build
"""


# ============================================================================
# ADDING EDUCATIONAL MATERIALS
# ============================================================================

"""
You have three ways to add materials to the knowledge base:

METHOD 1: Upload via API (Text)
================================
POST http://localhost:8000/api/v1/materials/add-text
Content-Type: application/json

{
    "title": "Chapter 5: Quadratic Equations",
    "content": "Long text content...",
    "subject": "Mathematics",
    "grade": 10
}


METHOD 2: Upload via API (File)
================================
POST http://localhost:8000/api/v1/materials/upload
Content-Type: multipart/form-data

[file upload]
Supported formats: PDF, DOCX, TXT


METHOD 3: Programmatically
===========================
import asyncio
from core.vector_store import VectorStore

async def add_materials():
    store = VectorStore()
    
    material_id = await store.add_text_material(
        content="Sinhala curriculum content...",
        title="Topic",
        subject="Mathematics",
        grade=10
    )
    print(f"Added: {material_id}")

asyncio.run(add_materials())
"""


# ============================================================================
# GENERATING EXAM PAPERS
# ============================================================================

"""
Basic Paper Generation:
=======================
POST http://localhost:8000/api/v1/papers/generate
Content-Type: application/json

{
    "subject": "Mathematics",
    "grade": 10,
    "num_questions": 10,
    "total_marks": 100,
    "difficulty_level": "medium",
    "language": "sinhala"
}


Advanced Options:
==================
{
    "subject": "Mathematics",
    "grade": 10,
    "num_questions": 15,
    "total_marks": 100,
    "difficulty_level": "mixed",  # easy, medium, hard, mixed
    "question_types": ["multiple_choice", "short_answer", "essay"],
    "include_explanation": true,
    "language": "sinhala",
    "custom_content": "Optional: specific curriculum content"
}


Batch Paper Generation:
=======================
POST http://localhost:8000/api/v1/papers/generate-batch?subject=Mathematics&grade=10&num_papers=3&num_questions=10

Returns 3 different exam papers for the same subject/grade
"""


# ============================================================================
# SEARCHING MATERIALS
# ============================================================================

"""
GET http://localhost:8000/api/v1/materials/search?query=quadratic%20equations&subject=Mathematics&grade=10

Returns most relevant material chunks from vector store
"""


# ============================================================================
# EXAM SUBMISSION
# ============================================================================

"""
POST http://localhost:8000/api/v1/exams/submit
Content-Type: application/json

{
    "exam_id": "paper_uuid",
    "student_id": "student_uuid",
    "answers": [
        {
            "question_id": "q_uuid_1",
            "answer": "Answer text"
        },
        {
            "question_id": "q_uuid_2",
            "answer": "Another answer"
        }
    ],
    "total_time_seconds": 3600
}
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
PROBLEM: "Module not found" error
SOLUTION: Activate virtual environment
$ source venv/bin/activate


PROBLEM: OpenAI API Key Error
SOLUTION: Check your .env file
$ cat .env | grep OPENAI_API_KEY
Ensure key is valid at https://platform.openai.com/api-keys


PROBLEM: FAISS import error
SOLUTION: Install CPU version
$ pip install faiss-cpu
Or GPU version:
$ pip install faiss-gpu


PROBLEM: Port 8000 already in use
SOLUTION: Use different port
$ uvicorn main:app --port 8001


PROBLEM: Sinhala text not displaying correctly
SOLUTION: Set environment variable
$ export PYTHONIOENCODING=utf-8


PROBLEM: Database connection errors
SOLUTION: Check PostgreSQL is running
$ docker-compose logs db
Verify DATABASE_URL in .env


PROBLEM: Vector store not working
SOLUTION: Check FAISS installation
import faiss
print(faiss.__version__)
Ensure data/vectors directory exists
$ mkdir -p data/vectors
"""


# ============================================================================
# PROJECT STRUCTURE REFERENCE
# ============================================================================

"""
sinhalaedu/
├── main.py                  # FastAPI app entry point
├── config.py                # Configuration management
├── models.py                # Database models (SQLAlchemy)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Container image
├── docker-compose.yml       # Multi-container setup
├── setup.sh                 # Setup script
├── quickstart.py            # Quick start script
│
├── api/
│   └── routes/
│       ├── papers.py        # Paper generation API
│       ├── materials.py     # Material management API
│       └── exams.py         # Exam submission API
│
├── schemas/                 # Pydantic models
│   ├── paper.py            # Paper/question schemas
│   ├── material.py         # Material schemas
│   └── exam.py             # Exam schemas
│
├── core/                    # Core business logic
│   ├── rag_pipeline.py     # RAG pipeline
│   ├── vector_store.py     # Vector store (FAISS)
│   └── embeddings.py       # Embedding service
│
├── utils/
│   └── sinhala.py          # Sinhala text utilities
│
├── data/
│   └── vectors/            # Vector store data
│
└── logs/                    # Application logs
"""


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

"""
1. Use GPU for embeddings:
   - Requires CUDA compatible GPU
   - pip install faiss-gpu
   - Significantly faster embedding generation

2. Cache frequent queries:
   - Enable Redis in docker-compose.yml
   - Reduces API calls to OpenAI

3. Use connection pooling:
   - Configure in DATABASE_URL
   - Improves database performance

4. Optimize chunk size:
   - Adjust CHUNK_SIZE in .env (default: 500)
   - Larger = better context, slower retrieval
   - Smaller = faster retrieval, less context

5. Use multiple workers:
   - Production: uvicorn main:app --workers 4
   - Handle more concurrent requests
   - Adjust based on CPU cores
"""


# ============================================================================
# NEXT STEPS
# ============================================================================

"""
1. ✅ Install and run application
2. 📚 Add educational materials for your subjects
3. 📝 Generate test papers
4. 👥 Set up student/teacher accounts (future)
5. 📊 Add analytics dashboard (future)
6. 🔒 Set up authentication (future)
7. 📈 Monitor usage and performance
"""


print(__doc__)
