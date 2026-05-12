"""Quick start guide and examples."""

# Example 1: Generate an exam paper
import asyncio
from schemas.paper import GeneratePaperRequest
from core.rag_pipeline import RAGPipeline

async def example_generate_paper():
    """Example: Generate a Sinhala exam paper."""
    rag = RAGPipeline()
    
    request = GeneratePaperRequest(
        subject="Mathematics",
        grade=10,
        num_questions=10,
        total_marks=100,
        difficulty_level="medium",
        language="sinhala",
    )
    
    paper = await rag.generate_paper(request)
    print(f"Generated paper: {paper.paper_id}")
    print(f"Title: {paper.title}")
    print(f"Total marks: {paper.total_marks}")
    return paper


# Example 2: Add material to vector store
async def example_add_material():
    """Example: Add Sinhala curriculum material."""
    from core.vector_store import VectorStore
    
    vector_store = VectorStore()
    
    sinhala_content = """
    ගණිතයේ පදනම්
    
    පූර්ණ සංඛ්‍යා යනු සියලු ධනාත්මක සඳහා උණාත්මක සුවිශේෂ සංඛ්‍යා හා ශුන්ය ඇතුළත් සංඛ්‍යා වේ.
    
    සරල සමීකරණ:
    ax + b = c
    
    පිළිතුර: x = (c - b) / a
    """
    
    material_id = await vector_store.add_text_material(
        content=sinhala_content,
        title="Mathematics Fundamentals",
        subject="Mathematics",
        grade=10,
    )
    
    print(f"Material added: {material_id}")
    return material_id


# Example 3: Search for relevant materials
async def example_search_materials():
    """Example: Search materials."""
    from core.vector_store import VectorStore
    
    vector_store = VectorStore()
    
    results = await vector_store.search(
        query="පූර්ණ සංඛ්‍යා සර්ව එකතුව",
        subject="Mathematics",
        grade=10,
        top_k=3,
    )
    
    print(f"Found {len(results)} results")
    for result in results:
        print(f"- {result['chunk_id']}: {result['content'][:100]}")
    
    return results


if __name__ == "__main__":
    print("Sinhala Exam Paper Generator - Examples")
    print("=" * 40)
    print()
    print("These examples show how to use the system.")
    print("Run them with: python examples.py")
    print()
    print("Available examples:")
    print("1. Generate exam paper")
    print("2. Add material to vector store")
    print("3. Search materials")
