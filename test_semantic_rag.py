#!/usr/bin/env python3
"""
Test script for Enhanced Semantic RAG
This script tests the intelligent search capabilities with conversational queries.
"""

from AGENT.multi_doc_processor import MultiDocumentProcessor
from semantic_rag import SemanticRAGProcessor

def test_semantic_rag():
    """Test the semantic RAG functionality with conversational queries."""
    print("🧪 Testing Enhanced Semantic RAG")
    print("=" * 60)
    
    docs_directory = "infos"
    
    # Load documents
    processor = MultiDocumentProcessor(docs_directory)
    if not processor.load_documents():
        print(f"❌ Failed to load documents from: {docs_directory}")
        return False
    
    print(f"✅ Documents loaded successfully from: {docs_directory}")
    
    # Initialize semantic RAG
    semantic_rag = SemanticRAGProcessor(processor)
    print("✅ Semantic RAG processor initialized")
    
    # Test conversational queries
    conversational_queries = [
        "Who is the main contact person?",
        "What are the payment terms?",
        "Tell me about the company",
        "What delivery issues have there been?",
        "How is the relationship with the client?",
        "Who handles purchasing?",
        "What's the financial situation?",
        "Are there any problems with logistics?",
        "What does the report say about steel?",
        "Who is Martin Vogel?"
    ]
    
    print(f"\n🔍 Testing conversational queries:")
    print("=" * 60)
    
    for i, query in enumerate(conversational_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        # Perform intelligent search
        results = semantic_rag.intelligent_search(query)
        
        if results['top_results']:
            print(f"✅ Found {results['total_results']} results")
            
            # Show intent analysis
            intent = results['intent']
            if intent['question_type']:
                print(f"   Question type: {intent['question_type']}")
            
            if intent['relevant_categories']:
                categories = [cat['category'] for cat in intent['relevant_categories'][:3]]
                print(f"   Relevant categories: {', '.join(categories)}")
            
            # Show top result
            top_result = results['top_results'][0]
            print(f"   Top result from {top_result['file_name']} (score: {top_result['relevance_score']}):")
            print(f"   {top_result['context'][:150]}...")
            
            # Show expanded search terms
            expanded_terms = intent['expanded_terms'][:5]
            print(f"   Search terms used: {', '.join(expanded_terms)}")
            
        else:
            print("❌ No results found")
            suggestions = semantic_rag.get_contextual_suggestions(query)
            if suggestions:
                print("   Suggestions:")
                for suggestion in suggestions:
                    print(f"     - {suggestion}")
    
    # Test document categorization
    print(f"\n📚 Document Categorization:")
    print("=" * 40)
    
    for category, info in semantic_rag.document_categories.items():
        if info['documents']:
            print(f"\n{category.upper()}: {info['description']}")
            for doc in info['documents']:
                print(f"  - {doc['file_name']} (relevance: {doc['relevance_score']})")
    
    print("\n✅ Semantic RAG test completed successfully!")
    return True

def test_query_expansion():
    """Test query expansion and synonym handling."""
    print(f"\n🔤 Testing Query Expansion:")
    print("=" * 40)
    
    docs_directory = "infos"
    processor = MultiDocumentProcessor(docs_directory)
    processor.load_documents()
    semantic_rag = SemanticRAGProcessor(processor)
    
    test_queries = [
        "company info",
        "contact person", 
        "payment details",
        "delivery problems",
        "procurement report"
    ]
    
    for query in test_queries:
        intent = semantic_rag._identify_query_intent(query)
        print(f"\nQuery: '{query}'")
        print(f"Expanded terms: {intent['expanded_terms']}")
        
        if intent['relevant_categories']:
            categories = [cat['category'] for cat in intent['relevant_categories'][:3]]
            print(f"Categories: {', '.join(categories)}")

if __name__ == "__main__":
    test_semantic_rag()
    test_query_expansion()
