#!/usr/bin/env python3
"""
Test script for OpenAI-Powered RAG
This script tests the OpenAI embeddings and semantic search capabilities.
"""

import os
from dotenv import load_dotenv
from AGENT.multi_doc_processor import MultiDocumentProcessor
from AGENT.openai_rag import OpenAIEnhancedRAG

# Load environment variables
load_dotenv('keys.env')

def test_openai_rag():
    """Test the OpenAI-powered RAG functionality."""
    print("🤖 Testing OpenAI-Powered RAG")
    print("=" * 60)
    
    # Check for OpenAI API key
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ OpenAI API key found: {openai_api_key[:10]}...")
    
    docs_directory = "infos"
    
    # Load documents
    processor = MultiDocumentProcessor(docs_directory)
    if not processor.load_documents():
        print(f"❌ Failed to load documents from: {docs_directory}")
        return False
    
    print(f"✅ Documents loaded successfully from: {docs_directory}")
    
    # Initialize OpenAI RAG
    openai_rag = OpenAIEnhancedRAG(openai_api_key)
    
    # Convert documents to the format expected by OpenAI RAG
    documents = []
    for doc in processor.documents:
        documents.append({
            'file_name': doc.file_name,
            'file_type': doc.file_type,
            'pages': doc.pages
        })
    
    # Load documents with OpenAI embeddings
    print("\n🔄 Creating OpenAI embeddings...")
    success = openai_rag.load_documents(documents, use_cache=False)  # Don't use cache for testing
    
    if not success:
        print("❌ Failed to create OpenAI embeddings")
        return False
    
    print("✅ OpenAI embeddings created successfully")
    
    # Test semantic search queries
    test_queries = [
        "Who is the main contact person?",
        "What are the payment terms?",
        "Tell me about TechParts company",
        "What delivery issues have there been?",
        "How is the relationship with the client?",
        "Who handles purchasing?",
        "What's the financial situation?",
        "Are there any problems with logistics?",
        "What does the report say about steel?",
        "Who is Martin Vogel?",
        "What are the communication preferences?",
        "Tell me about the procurement process"
    ]
    
    print(f"\n🔍 Testing semantic search queries:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 50)
        
        # Perform intelligent search
        results = openai_rag.intelligent_search(query)
        
        if results.get('found', False):
            print(f"✅ Found {results['total_results']} results")
            print(f"   Summary: {results['summary']}")
            
            # Show top result
            if results['key_insights']:
                top_insight = results['key_insights'][0]
                print(f"   Top result from {top_insight['file_name']} (similarity: {top_insight['similarity']}):")
                print(f"   {top_insight['content'][:200]}...")
                
                # Show all insights
                print(f"   All insights:")
                for insight in results['key_insights'][:3]:  # Show top 3
                    print(f"     - {insight['file_name']} (page {insight['page_number']}): {insight['similarity']:.3f} similarity")
        else:
            print(f"❌ {results.get('message', 'No results found')}")
    
    # Test document summary
    print(f"\n📚 Document Summary:")
    print("=" * 40)
    
    summary = openai_rag.get_summary()
    print(f"Total chunks: {summary['total_chunks']}")
    print(f"Total files: {summary['total_files']}")
    
    for file_info in summary['files']:
        print(f"  - {file_info['file_name']} ({file_info['file_type']}): {file_info['chunks']} chunks, {file_info['total_words']} words")
    
    print("\n✅ OpenAI RAG test completed successfully!")
    return True

def test_embedding_similarity():
    """Test embedding similarity with specific examples."""
    print(f"\n🎯 Testing Embedding Similarity:")
    print("=" * 50)
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found")
        return
    
    from AGENT.openai_rag import OpenAIEmbeddingProcessor
    
    processor = OpenAIEmbeddingProcessor(openai_api_key)
    
    # Test similarity between related terms
    test_pairs = [
        ("company", "business"),
        ("contact person", "Martin Vogel"),
        ("payment terms", "Net 45"),
        ("delivery issues", "logistics problems"),
        ("procurement", "purchasing"),
        ("TechParts", "tech parts"),
        ("ProcureMind", "procure mind")
    ]
    
    for term1, term2 in test_pairs:
        embedding1 = processor.get_embedding(term1)
        embedding2 = processor.get_embedding(term2)
        
        if embedding1 and embedding2:
            similarity = processor.cosine_similarity(embedding1, embedding2)
            print(f"   '{term1}' vs '{term2}': {similarity:.3f} similarity")
        else:
            print(f"   '{term1}' vs '{term2}': Error getting embeddings")

if __name__ == "__main__":
    test_openai_rag()
    test_embedding_similarity()
