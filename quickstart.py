"""Quick start script to test the application."""

import asyncio
from core.vector_store import VectorStore
from schemas.paper import GeneratePaperRequest
from core.rag_pipeline import RAGPipeline


async def main():
    """Run quick start examples."""
    print("\n" + "="*60)
    print("🎓 Sinhala Exam Paper Generator - Quick Start")
    print("="*60 + "\n")
    
    # Initialize components
    rag = RAGPipeline()
    vector_store = VectorStore()
    
    # Step 1: Add sample Sinhala material
    print("📚 Step 1: Adding sample Sinhala material...")
    sample_content = """
    ගණිතයේ පදනම්
    
    පූර්ණ සංඛ්‍යා: සියලු ධනාත්මක සහ ඍණාත්මක සුවිශේෂ සංඛ්‍යා හා ශුන්ය ඇතුළත්.
    
    සරල සමීකරණ (ax + b = c):
    - x = (c - b) / a
    - a ≠ 0 විය යුතුයි
    
    පිටවරණ ගුණ:
    - සංකලනයේ සහකාරී ගුණ: (a + b) + c = a + (b + c)
    - ගුණයේ සහකාරී ගුණ: (a × b) × c = a × (b × c)
    - බෙදා දෙන ගුණ: a × (b + c) = (a × b) + (a × c)
    """
    
    try:
        material_id = await vector_store.add_text_material(
            content=sample_content,
            title="Mathematics Grade 10 - Fundamentals",
            subject="Mathematics",
            grade=10,
        )
        print(f"✓ Material added: {material_id}\n")
    except Exception as e:
        print(f"Note: Vector store not fully configured yet: {e}\n")
    
    # Step 2: Generate an exam paper
    print("📝 Step 2: Generating Sinhala exam paper...")
    
    request = GeneratePaperRequest(
        subject="Mathematics",
        grade=10,
        num_questions=5,
        total_marks=50,
        difficulty_level="medium",
        language="sinhala",
        include_explanation=True,
    )
    
    try:
        paper = await rag.generate_paper(request)
        
        print(f"✓ Paper generated!")
        print(f"  - Paper ID: {paper.paper_id}")
        print(f"  - Title: {paper.title}")
        print(f"  - Questions: {len(paper.questions)}")
        print(f"  - Total Marks: {paper.total_marks}")
        print(f"  - Duration: {paper.duration_minutes} minutes\n")
        
        # Display questions
        print("📋 Questions:")
        print("-" * 60)
        for i, q in enumerate(paper.questions, 1):
            print(f"\n{i}. {q.question_text}")
            print(f"   Type: {q.question_type.value}")
            print(f"   Marks: {q.marks}")
            if q.options:
                for j, opt in enumerate(q.options, 1):
                    print(f"   {chr(96+j)}) {opt}")
        
    except Exception as e:
        print(f"Note: Full generation requires OpenAI API key: {e}\n")
    
    print("\n" + "="*60)
    print("✅ Quick start complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Set up your .env file with OPENAI_API_KEY")
    print("2. Run: python main.py")
    print("3. Visit: http://localhost:8000/docs")
    print("4. Try API endpoints in Swagger UI")
    print("\nDocumentation:")
    print("- See README.md for full documentation")
    print("- Check examples.py for more examples")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
