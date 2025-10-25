#!/usr/bin/env python3
"""
Test script for Multi-Document functionality
This script tests the multi-document processor with the infos folder.
"""

from multi_doc_processor import MultiDocumentProcessor

def test_multi_doc_processor():
    """Test the multi-document processor functionality."""
    print("🧪 Testing Multi-Document Processor")
    print("=" * 50)
    
    docs_directory = "infos"
    
    # Test multi-document loading
    processor = MultiDocumentProcessor(docs_directory)
    if not processor.load_documents():
        print(f"❌ Failed to load documents from: {docs_directory}")
        return False
    
    print(f"✅ Documents loaded successfully from: {docs_directory}")
    
    # Test summary
    summary = processor.get_document_summary()
    print(f"\n📚 Documents Summary:")
    print(f"   Total documents: {summary['total_documents']}")
    print(f"   Total pages: {summary['total_pages']}")
    print(f"   Total words: {summary['total_words']}")
    
    print(f"\n📄 Individual Documents:")
    for doc in summary['documents']:
        print(f"   - {doc['file_name']} ({doc['file_type']}): {doc['total_pages']} pages, {doc['total_words']} words")
    
    # Test search functionality across all documents
    test_queries = ["TechParts", "Martin Vogel", "Net 45", "procurement", "steel"]
    
    print(f"\n🔍 Testing search across all documents:")
    for query in test_queries:
        print(f"\n   Searching for: '{query}'")
        results = processor.search_all_documents(query)
        print(f"   Found {len(results)} results across all documents")
        
        if results:
            # Show first result
            first_result = results[0]
            print(f"   First result from {first_result['file_name']} (page {first_result['page_number']}):")
            print(f"   {first_result['context'][:150]}...")
    
    # Test specific document search
    print(f"\n🔍 Testing search in specific document:")
    text_file_results = processor.search_in_document("summary.txt", "Martin Vogel")
    print(f"   Found {len(text_file_results)} results for 'Martin Vogel' in summary.txt")
    
    if text_file_results:
        print(f"   Context: {text_file_results[0]['context'][:200]}...")
    
    # Test document content retrieval
    print(f"\n📖 Testing document content retrieval:")
    content = processor.get_document_content("summary.txt")
    if content:
        print(f"   Retrieved content from summary.txt: {len(content.split())} words")
        print(f"   First 200 chars: {content[:200]}...")
    
    print("\n✅ Multi-document processor test completed successfully!")
    return True

if __name__ == "__main__":
    test_multi_doc_processor()
