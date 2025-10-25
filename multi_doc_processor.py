#!/usr/bin/env python3
"""
Multi-Document Processor for LiveKit Agent
This module handles multiple PDFs and text files from a directory.
"""

import os
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

class DocumentProcessor:
    """Processes individual documents (PDF or text files)."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_type = self._get_file_type()
        self.content = ""
        self.pages = []
        self.loaded = False
        
    def _get_file_type(self) -> str:
        """Determine file type based on extension."""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == '.pdf':
            return 'pdf'
        elif ext in ['.txt', '.md']:
            return 'text'
        else:
            return 'unknown'
    
    def load(self) -> bool:
        """Load content from the document."""
        try:
            if self.file_type == 'pdf':
                return self._load_pdf()
            elif self.file_type == 'text':
                return self._load_text()
            else:
                return False
        except Exception as e:
            print(f"Error loading {self.file_path}: {e}")
            return False
    
    def _load_pdf(self) -> bool:
        """Load content from PDF file."""
        pdf_document = fitz.open(self.file_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            self.pages.append({
                'page_number': page_num + 1,
                'text': text,
                'word_count': len(text.split())
            })
            self.content += f"\n--- Page {page_num + 1} ---\n{text}\n"
        
        pdf_document.close()
        self.loaded = True
        return True
    
    def _load_text(self) -> bool:
        """Load content from text file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into logical sections (by paragraphs or lines)
        sections = content.split('\n\n')
        for i, section in enumerate(sections):
            if section.strip():
                self.pages.append({
                    'page_number': i + 1,
                    'text': section.strip(),
                    'word_count': len(section.split())
                })
        
        self.content = content
        self.loaded = True
        return True
    
    def search_text(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search for text in the document."""
        if not self.loaded:
            return []
        
        query = query if case_sensitive else query.lower()
        results = []
        
        for page in self.pages:
            page_text = page['text'] if case_sensitive else page['text'].lower()
            
            if query in page_text:
                pos = page_text.find(query)
                context_start = max(0, pos - 100)
                context_end = min(len(page['text']), pos + len(query) + 100)
                context = page['text'][context_start:context_end]
                
                results.append({
                    'file_name': self.file_name,
                    'file_type': self.file_type,
                    'page_number': page['page_number'],
                    'context': context,
                    'position': pos,
                    'query': query
                })
        
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get document summary."""
        if not self.loaded:
            return {}
        
        total_words = sum(page['word_count'] for page in self.pages)
        
        return {
            'file_name': self.file_name,
            'file_type': self.file_type,
            'total_pages': len(self.pages),
            'total_words': total_words,
            'file_size': os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0
        }


class MultiDocumentProcessor:
    """Processes multiple documents from a directory."""
    
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.documents: List[DocumentProcessor] = []
        self.loaded = False
        
    def load_documents(self) -> bool:
        """Load all supported documents from the directory."""
        try:
            if not os.path.exists(self.directory_path):
                print(f"Directory not found: {self.directory_path}")
                return False
            
            # Find all supported files
            supported_extensions = ['.pdf', '.txt', '.md']
            files_found = []
            
            for file_path in Path(self.directory_path).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    files_found.append(str(file_path))
            
            if not files_found:
                print(f"No supported documents found in {self.directory_path}")
                return False
            
            # Load each document
            for file_path in files_found:
                doc = DocumentProcessor(file_path)
                if doc.load():
                    self.documents.append(doc)
                    print(f"✅ Loaded: {doc.file_name} ({doc.file_type})")
                else:
                    print(f"❌ Failed to load: {file_path}")
            
            self.loaded = len(self.documents) > 0
            return self.loaded
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return False
    
    def search_all_documents(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search across all loaded documents."""
        if not self.loaded:
            return []
        
        all_results = []
        for doc in self.documents:
            results = doc.search_text(query, case_sensitive)
            all_results.extend(results)
        
        # Sort by relevance (shorter context = more relevant)
        all_results.sort(key=lambda x: len(x['context']))
        
        return all_results
    
    def get_document_summary(self) -> Dict[str, Any]:
        """Get summary of all documents."""
        if not self.loaded:
            return {}
        
        total_docs = len(self.documents)
        total_pages = sum(len(doc.pages) for doc in self.documents)
        total_words = sum(sum(page['word_count'] for page in doc.pages) for doc in self.documents)
        
        doc_summaries = [doc.get_summary() for doc in self.documents]
        
        return {
            'directory': self.directory_path,
            'total_documents': total_docs,
            'total_pages': total_pages,
            'total_words': total_words,
            'documents': doc_summaries
        }
    
    def get_document_by_name(self, file_name: str) -> Optional[DocumentProcessor]:
        """Get a specific document by filename."""
        for doc in self.documents:
            if doc.file_name == file_name:
                return doc
        return None
    
    def search_in_document(self, file_name: str, query: str) -> List[Dict[str, Any]]:
        """Search within a specific document."""
        doc = self.get_document_by_name(file_name)
        if doc:
            return doc.search_text(query)
        return []
    
    def get_document_content(self, file_name: str, page_number: Optional[int] = None) -> Optional[str]:
        """Get content from a specific document."""
        doc = self.get_document_by_name(file_name)
        if not doc:
            return None
        
        if page_number:
            for page in doc.pages:
                if page['page_number'] == page_number:
                    return page['text']
            return None
        else:
            return doc.content


# Global multi-document processor instance
multi_doc_processor: Optional[MultiDocumentProcessor] = None

def initialize_multi_documents(directory_path: str) -> bool:
    """Initialize the global multi-document processor."""
    global multi_doc_processor
    multi_doc_processor = MultiDocumentProcessor(directory_path)
    return multi_doc_processor.load_documents()

def get_multi_doc_processor() -> Optional[MultiDocumentProcessor]:
    """Get the global multi-document processor instance."""
    return multi_doc_processor
