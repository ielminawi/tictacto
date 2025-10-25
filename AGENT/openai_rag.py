#!/usr/bin/env python3
"""
OpenAI-Powered Document Processing with Embeddings
This module uses OpenAI embeddings for semantic document search and information extraction.
"""

import os
import openai
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import json
import pickle
from pathlib import Path
import re
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DocumentChunk:
    """Represents a chunk of document with its embedding."""
    content: str
    file_name: str
    file_type: str
    page_number: int
    chunk_index: int
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None

class OpenAIEmbeddingProcessor:
    """Processes documents using OpenAI embeddings for semantic search."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.chunks: List[DocumentChunk] = []
        self.embeddings_cache_file = "embeddings_cache.pkl"
        
    def chunk_document(self, content: str, file_name: str, file_type: str, page_number: int, 
                      chunk_size: int = 1000, overlap: int = 200) -> List[DocumentChunk]:
        """Split document content into overlapping chunks."""
        chunks = []
        
        # Split content into sentences for better chunking
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(DocumentChunk(
                    content=current_chunk.strip(),
                    file_name=file_name,
                    file_type=file_type,
                    page_number=page_number,
                    chunk_index=chunk_index,
                    metadata={
                        'word_count': len(current_chunk.split()),
                        'char_count': len(current_chunk)
                    }
                ))
                chunk_index += 1
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                file_name=file_name,
                file_type=file_type,
                page_number=page_number,
                chunk_index=chunk_index,
                metadata={
                    'word_count': len(current_chunk.split()),
                    'char_count': len(current_chunk)
                }
            ))
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI API."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def process_documents(self, documents: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """Process all documents and create embeddings."""
        all_chunks = []
        
        print("🔄 Processing documents with OpenAI embeddings...")
        
        for doc in documents:
            print(f"   Processing {doc['file_name']} ({doc['file_type']})...")
            
            # Create chunks for each page
            for page in doc['pages']:
                chunks = self.chunk_document(
                    content=page['text'],
                    file_name=doc['file_name'],
                    file_type=doc['file_type'],
                    page_number=page['page_number']
                )
                
                # Get embeddings for each chunk
                for chunk in chunks:
                    embedding = self.get_embedding(chunk.content)
                    chunk.embedding = embedding
                    all_chunks.append(chunk)
        
        self.chunks = all_chunks
        print(f"✅ Created {len(all_chunks)} chunks with embeddings")
        
        # Cache embeddings
        self.save_embeddings_cache()
        
        return all_chunks
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search using embeddings."""
        if not self.chunks:
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        if not query_embedding:
            return []
        
        # Calculate similarities
        similarities = []
        for chunk in self.chunks:
            if chunk.embedding:
                similarity = self.cosine_similarity(query_embedding, chunk.embedding)
                similarities.append({
                    'chunk': chunk,
                    'similarity': similarity
                })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top results
        results = []
        for item in similarities[:top_k]:
            chunk = item['chunk']
            results.append({
                'content': chunk.content,
                'file_name': chunk.file_name,
                'file_type': chunk.file_type,
                'page_number': chunk.page_number,
                'chunk_index': chunk.chunk_index,
                'similarity': item['similarity'],
                'metadata': chunk.metadata
            })
        
        return results
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def extract_key_information(self, query: str) -> Dict[str, Any]:
        """Extract key information related to a query using semantic search."""
        results = self.semantic_search(query, top_k=8)
        
        if not results:
            return {
                'query': query,
                'found': False,
                'message': f"No relevant information found for '{query}'"
            }
        
        # Group results by file
        results_by_file = {}
        for result in results:
            file_name = result['file_name']
            if file_name not in results_by_file:
                results_by_file[file_name] = []
            results_by_file[file_name].append(result)
        
        # Extract key insights
        key_insights = []
        for file_name, file_results in results_by_file.items():
            # Get the most relevant result from this file
            best_result = max(file_results, key=lambda x: x['similarity'])
            
            key_insights.append({
                'file_name': file_name,
                'file_type': best_result['file_type'],
                'page_number': best_result['page_number'],
                'content': best_result['content'],
                'similarity': best_result['similarity'],
                'relevance': 'high' if best_result['similarity'] > 0.8 else 'medium'
            })
        
        return {
            'query': query,
            'found': True,
            'total_results': len(results),
            'key_insights': key_insights,
            'summary': f"Found {len(key_insights)} relevant documents with information about '{query}'"
        }
    
    def get_document_summary(self) -> Dict[str, Any]:
        """Get a summary of all processed documents."""
        if not self.chunks:
            return {}
        
        # Group chunks by file
        files = {}
        for chunk in self.chunks:
            if chunk.file_name not in files:
                files[chunk.file_name] = {
                    'file_name': chunk.file_name,
                    'file_type': chunk.file_type,
                    'chunks': 0,
                    'total_words': 0,
                    'pages': set()
                }
            
            files[chunk.file_name]['chunks'] += 1
            files[chunk.file_name]['total_words'] += chunk.metadata.get('word_count', 0)
            files[chunk.file_name]['pages'].add(chunk.page_number)
        
        # Convert sets to lists for JSON serialization
        for file_info in files.values():
            file_info['pages'] = sorted(list(file_info['pages']))
        
        return {
            'total_chunks': len(self.chunks),
            'total_files': len(files),
            'files': list(files.values())
        }
    
    def save_embeddings_cache(self):
        """Save embeddings to cache file."""
        try:
            cache_data = {
                'chunks': self.chunks,
                'timestamp': datetime.now().isoformat(),
                'model': self.model
            }
            with open(self.embeddings_cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            print(f"✅ Embeddings cached to {self.embeddings_cache_file}")
        except Exception as e:
            print(f"❌ Error saving cache: {e}")
    
    def load_embeddings_cache(self) -> bool:
        """Load embeddings from cache file."""
        try:
            if os.path.exists(self.embeddings_cache_file):
                with open(self.embeddings_cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                
                self.chunks = cache_data['chunks']
                print(f"✅ Loaded {len(self.chunks)} chunks from cache")
                return True
        except Exception as e:
            print(f"❌ Error loading cache: {e}")
        
        return False
    
    def clear_cache(self):
        """Clear the embeddings cache."""
        if os.path.exists(self.embeddings_cache_file):
            os.remove(self.embeddings_cache_file)
            print("✅ Cache cleared")


class OpenAIEnhancedRAG:
    """Enhanced RAG system using OpenAI embeddings."""
    
    def __init__(self, api_key: str):
        self.processor = OpenAIEmbeddingProcessor(api_key)
        self.documents_loaded = False
    
    def load_documents(self, documents: List[Dict[str, Any]], use_cache: bool = True) -> bool:
        """Load and process documents with embeddings."""
        if use_cache and self.processor.load_embeddings_cache():
            self.documents_loaded = True
            return True
        
        # Process documents with embeddings
        chunks = self.processor.process_documents(documents)
        self.documents_loaded = len(chunks) > 0
        
        return self.documents_loaded
    
    def intelligent_search(self, query: str) -> Dict[str, Any]:
        """Perform intelligent semantic search."""
        if not self.documents_loaded:
            return {
                'error': 'Documents not loaded. Please load documents first.',
                'query': query
            }
        
        # Extract key information using semantic search
        result = self.processor.extract_key_information(query)
        
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of processed documents."""
        return self.processor.get_document_summary()
