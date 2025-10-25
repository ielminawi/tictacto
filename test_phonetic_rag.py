#!/usr/bin/env python3
"""
Test script for Enhanced Semantic RAG with Phonetic Matching
This script tests the phonetic matching and fuzzy string matching capabilities.
"""

from AGENT.multi_doc_processor import MultiDocumentProcessor
from enhanced_semantic_rag import EnhancedSemanticRAGProcessor, PhoneticMatcher

def test_phonetic_matcher():
    """Test the phonetic matcher with common mishearings."""
    print("🔤 Testing Phonetic Matcher")
    print("=" * 50)
    
    matcher = PhoneticMatcher()
    
    # Test common mishearings
    test_queries = [
        "tech parts",      # Should match "techparts"
        "tech-parts",      # Should match "techparts"
        "procure mind",    # Should match "procuremind"
        "procure-mind",    # Should match "procuremind"
        "steel core",      # Should match "steelcore"
        "steel-core",      # Should match "steelcore"
        "marten",          # Should match "martin"
        "martyn",          # Should match "martin"
        "vogal",           # Should match "vogel"
        "vogul",           # Should match "vogel"
        "gmb",             # Should match "gmbh"
        "tech parts gmbh", # Should match "techparts gmbh"
        "procure mind client report", # Should match "procuremind client report"
        "steel core report" # Should match "steelcore report"
    ]
    
    for query in test_queries:
        matches = matcher.find_matches(query)
        print(f"\nQuery: '{query}'")
        print(f"Matches: {matches[:5]}")  # Show first 5 matches
        
        # Test Soundex
        soundex = matcher.simple_soundex(query)
        print(f"Soundex: {soundex}")
    
    print("\n✅ Phonetic matcher test completed!")

def test_enhanced_semantic_rag():
    """Test the enhanced semantic RAG with phonetic matching."""
    print("\n🧪 Testing Enhanced Semantic RAG with Phonetic Matching")
    print("=" * 70)
    
    docs_directory = "infos"
    
    # Load documents
    processor = MultiDocumentProcessor(docs_directory)
    if not processor.load_documents():
        print(f"❌ Failed to load documents from: {docs_directory}")
        return False
    
    print(f"✅ Documents loaded successfully from: {docs_directory}")
    
    # Initialize enhanced semantic RAG
    semantic_rag = EnhancedSemanticRAGProcessor(processor)
    print("✅ Enhanced Semantic RAG processor initialized")
    
    # Test queries with common mishearings
    misheard_queries = [
        "Tell me about tech parts",           # Should find TechParts GmbH info
        "What does procure mind say?",        # Should find ProcureMind report
        "Show me steel core information",     # Should find SteelCore report
        "Who is marten vogal?",              # Should find Martin Vogel
        "What are the payment terms for tech parts gmbh?", # Should find payment info
        "Tell me about the procure mind steel core report", # Should find report
        "Who handles purchasing at tech parts?", # Should find Martin Vogel
        "What's in the steel core document?", # Should find SteelCore report
        "Show me procure mind analysis",      # Should find ProcureMind analysis
        "Who is the contact at tech parts gmbh?" # Should find Martin Vogel
    ]
    
    print(f"\n🔍 Testing misheard company name queries:")
    print("=" * 70)
    
    for i, query in enumerate(misheard_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 50)
        
        # Perform intelligent search
        results = semantic_rag.intelligent_search(query)
        
        if results['top_results']:
            print(f"✅ Found {results['total_results']} results")
            
            # Show phonetic matches used
            if 'phonetic_matches' in results and len(results['phonetic_matches']) > 1:
                print(f"   Phonetic matches used: {results['phonetic_matches'][:5]}")
            
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
            
        else:
            print("❌ No results found")
            suggestions = semantic_rag.get_contextual_suggestions(query)
            if suggestions:
                print("   Suggestions:")
                for suggestion in suggestions:
                    print(f"     - {suggestion}")
    
    # Test Soundex matching
    print(f"\n🔊 Testing Soundex Matching:")
    print("=" * 40)
    
    soundex_tests = [
        ("techparts", "tech parts"),
        ("procuremind", "procure mind"),
        ("steelcore", "steel core"),
        ("martin", "marten"),
        ("vogel", "vogal")
    ]
    
    for original, misheard in soundex_tests:
        original_soundex = semantic_rag.phonetic_matcher.simple_soundex(original)
        misheard_soundex = semantic_rag.phonetic_matcher.simple_soundex(misheard)
        match = original_soundex == misheard_soundex
        
        print(f"   '{original}' ({original_soundex}) vs '{misheard}' ({misheard_soundex}): {'✅' if match else '❌'}")
    
    print("\n✅ Enhanced Semantic RAG test completed successfully!")
    return True

def test_fuzzy_matching():
    """Test fuzzy string matching capabilities."""
    print(f"\n🎯 Testing Fuzzy String Matching:")
    print("=" * 50)
    
    matcher = PhoneticMatcher()
    
    fuzzy_tests = [
        ("techparts", "tech parts", 0.7),
        ("procuremind", "procure mind", 0.7),
        ("steelcore", "steel core", 0.7),
        ("martin", "marten", 0.7),
        ("vogel", "vogal", 0.7),
        ("gmbh", "gmb", 0.7)
    ]
    
    for original, misheard, threshold in fuzzy_tests:
        match = matcher.fuzzy_match(original, misheard, threshold)
        similarity = matcher.fuzzy_match(original, misheard, 0.0)  # Get actual similarity
        print(f"   '{original}' vs '{misheard}': {similarity:.2f} similarity, {'✅' if match else '❌'} match")

if __name__ == "__main__":
    test_phonetic_matcher()
    test_enhanced_semantic_rag()
    test_fuzzy_matching()
