"""
API Usage Examples
Sinhala Exam Paper Generator
"""

import requests
import json
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

# =============================================================================
# EXAMPLE 1: Health Check
# =============================================================================
print("EXAMPLE 1: Health Check")
print("-" * 60)

response = requests.get("http://localhost:8000/health")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()


# =============================================================================
# EXAMPLE 2: List Available Subjects
# =============================================================================
print("EXAMPLE 2: List Available Subjects")
print("-" * 60)

response = requests.get(f"{BASE_URL}/papers/subjects", params={"language": "sinhala"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()


# =============================================================================
# EXAMPLE 3: Generate Exam Paper (Basic)
# =============================================================================
print("EXAMPLE 3: Generate Sinhala Exam Paper")
print("-" * 60)

paper_request = {
    "subject": "Mathematics",
    "grade": 10,
    "num_questions": 5,
    "total_marks": 50,
    "difficulty_level": "medium",
    "language": "sinhala"
}

print(f"Request: {json.dumps(paper_request, indent=2)}")
print()

# Note: Requires OpenAI API key configured
# response = requests.post(f"{BASE_URL}/papers/generate", json=paper_request)
# if response.status_code == 200:
#     paper = response.json()
#     print(f"Generated Paper ID: {paper['paper_id']}")
#     print(f"Title: {paper['title']}")
#     print(f"Questions: {len(paper['questions'])}")
#     for q in paper['questions']:
#         print(f"\n  {q['question_text']}")
#         print(f"  Marks: {q['marks']}")


# =============================================================================
# EXAMPLE 4: Generate Exam Paper (Advanced)
# =============================================================================
print("EXAMPLE 4: Advanced Paper Generation")
print("-" * 60)

advanced_request = {
    "subject": "Science",
    "grade": 11,
    "num_questions": 15,
    "total_marks": 100,
    "question_types": ["multiple_choice", "short_answer", "essay"],
    "difficulty_level": "mixed",
    "include_explanation": True,
    "language": "sinhala"
}

print(f"Request: {json.dumps(advanced_request, indent=2)}")
print()


# =============================================================================
# EXAMPLE 5: Add Text Material
# =============================================================================
print("EXAMPLE 5: Add Sinhala Material to Knowledge Base")
print("-" * 60)

material_request = {
    "title": "Quadratic Equations",
    "content": """
    චතුරස්‍ර සමීකරණ
    
    ax² + bx + c = 0 වර්ගයේ සමීකරණ චතුරස්‍ර සමීකරණ ලෙස හැඳින්වේ.
    
    විසඳුම් සූත්‍රය:
    x = (-b ± √(b² - 4ac)) / 2a
    
    විවිධ අවස්තා:
    1. b² - 4ac > 0: තනි බිමට පතන පූර්ණ විසඳුම් දෙකක්
    2. b² - 4ac = 0: එක තනි විසඳුමක්
    3. b² - 4ac < 0: සංකීර්ණ විසඳුම්
    """,
    "subject": "Mathematics",
    "grade": 10
}

print(f"Request: {json.dumps(material_request, indent=2)}")
print()
# response = requests.post(f"{BASE_URL}/materials/add-text", json=material_request)
# if response.status_code == 200:
#     print(f"Material added: {response.json()['material_id']}")


# =============================================================================
# EXAMPLE 6: Search Materials
# =============================================================================
print("EXAMPLE 6: Search Educational Materials")
print("-" * 60)

search_params = {
    "query": "චතුරස්‍ර සමීකරණ විසඳුම්",
    "subject": "Mathematics",
    "grade": 10,
    "top_k": 5
}

print(f"Search Query: {search_params['query']}")
print(f"Subject: {search_params['subject']}")
print(f"Grade: {search_params['grade']}")
print()

# response = requests.get(f"{BASE_URL}/materials/search", params=search_params)
# if response.status_code == 200:
#     results = response.json()
#     print(f"Found {results['count']} results")
#     for result in results['results']:
#         print(f"\n  Score: {result['score']}")
#         print(f"  Content: {result['content'][:100]}...")


# =============================================================================
# EXAMPLE 7: Upload File Material
# =============================================================================
print("EXAMPLE 7: Upload Material File")
print("-" * 60)

print("""
curl -X POST "http://localhost:8000/api/v1/materials/upload" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@curriculum_chapter.pdf"
""")
print()


# =============================================================================
# EXAMPLE 8: List All Materials
# =============================================================================
print("EXAMPLE 8: List All Materials")
print("-" * 60)

list_params = {
    "subject": "Mathematics",
    "grade": 10
}

print(f"Filters: {list_params}")
# response = requests.get(f"{BASE_URL}/materials/materials", params=list_params)
# if response.status_code == 200:
#     materials = response.json()
#     print(f"Found {materials['count']} materials")
print()


# =============================================================================
# EXAMPLE 9: Generate Batch of Papers
# =============================================================================
print("EXAMPLE 9: Generate Multiple Exam Papers")
print("-" * 60)

batch_params = {
    "subject": "History",
    "grade": 9,
    "num_papers": 3,
    "num_questions": 10
}

print(f"Batch Generation Parameters:")
for key, value in batch_params.items():
    print(f"  {key}: {value}")
print()

# response = requests.post(
#     f"{BASE_URL}/papers/generate-batch",
#     params=batch_params
# )
# if response.status_code == 200:
#     result = response.json()
#     print(f"Generated {result['count']} papers")


# =============================================================================
# EXAMPLE 10: Preview Generated Paper
# =============================================================================
print("EXAMPLE 10: Preview Generated Paper")
print("-" * 60)

paper_id = "550e8400-e29b-41d4-a716-446655440000"  # Example UUID
print(f"Paper ID: {paper_id}")

# response = requests.get(f"{BASE_URL}/papers/preview/{paper_id}")
# if response.status_code == 200:
#     paper = response.json()
#     print(json.dumps(paper, indent=2, ensure_ascii=False))


# =============================================================================
# EXAMPLE 11: Submit Exam for Grading
# =============================================================================
print("EXAMPLE 11: Submit Exam Answers")
print("-" * 60)

exam_submission = {
    "exam_id": "exam-uuid-1234",
    "student_id": "student-uuid-5678",
    "answers": [
        {
            "question_id": "q-1",
            "answer": "The answer to question 1",
            "time_spent_seconds": 120
        },
        {
            "question_id": "q-2",
            "answer": "The answer to question 2",
            "time_spent_seconds": 180
        }
    ],
    "total_time_seconds": 3600
}

print(f"Request: {json.dumps(exam_submission, indent=2)}")
print()


# =============================================================================
# EXAMPLE 12: Get Exam Results
# =============================================================================
print("EXAMPLE 12: Get Exam Results")
print("-" * 60)

exam_id = "exam-uuid-1234"
print(f"Retrieving results for Exam ID: {exam_id}")

# response = requests.get(f"{BASE_URL}/exams/results/{exam_id}")
# if response.status_code == 200:
#     results = response.json()
#     print(json.dumps(results, indent=2))


# =============================================================================
# EXAMPLE 13: Get Analytics
# =============================================================================
print("EXAMPLE 13: Get Exam Statistics")
print("-" * 60)

analytics_params = {
    "subject": "Mathematics",
    "grade": 10,
    "time_period": "month"
}

print(f"Analytics Parameters: {analytics_params}")
# response = requests.get(f"{BASE_URL}/exams/statistics", params=analytics_params)
# if response.status_code == 200:
#     stats = response.json()
#     print(json.dumps(stats, indent=2))


# =============================================================================
# PYTHON CLIENT EXAMPLE
# =============================================================================
print("\nEXAMPLE 14: Python Client Implementation")
print("-" * 60)

code_example = '''
import asyncio
from schemas.paper import GeneratePaperRequest
from core.rag_pipeline import RAGPipeline

async def generate_sinhala_paper():
    """Generate a Sinhala exam paper programmatically."""
    rag = RAGPipeline()
    
    request = GeneratePaperRequest(
        subject="Geography",
        grade=9,
        num_questions=10,
        total_marks=75,
        difficulty_level="medium",
        language="sinhala"
    )
    
    paper = await rag.generate_paper(request)
    
    print(f"Generated: {paper.title}")
    print(f"Questions: {len(paper.questions)}")
    
    for i, question in enumerate(paper.questions, 1):
        print(f"\\n{i}. {question.question_text}")
        print(f"   Marks: {question.marks}")
        if question.options:
            for j, opt in enumerate(question.options, 1):
                print(f"   {chr(96+j)}) {opt}")

# Run
asyncio.run(generate_sinhala_paper())
'''

print(code_example)
print()


# =============================================================================
# CURL EXAMPLES
# =============================================================================
print("\nEXAMPLE 15: cURL Commands")
print("-" * 60)

curl_examples = '''
# Health Check
curl http://localhost:8000/health

# List Subjects
curl "http://localhost:8000/api/v1/papers/subjects?language=sinhala"

# Generate Paper (with JSON data)
curl -X POST http://localhost:8000/api/v1/papers/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "subject": "Mathematics",
    "grade": 10,
    "num_questions": 5,
    "total_marks": 50,
    "language": "sinhala"
  }'

# Search Materials
curl "http://localhost:8000/api/v1/materials/search?query=quadratic&subject=Mathematics&grade=10"

# Add Text Material
curl -X POST http://localhost:8000/api/v1/materials/add-text \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Chapter Title",
    "content": "Material content here...",
    "subject": "Mathematics",
    "grade": 10
  }'

# Swagger UI Documentation
open http://localhost:8000/docs
'''

print(curl_examples)
print()


print("=" * 60)
print("For more examples and documentation:")
print("- Visit: http://localhost:8000/docs (Swagger UI)")
print("- Read: README.md")
print("- Read: SETUP_GUIDE.md")
print("=" * 60)
