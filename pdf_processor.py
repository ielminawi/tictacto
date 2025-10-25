#!/usr/bin/env python3
"""
PDF Processor for LiveKit Agent
This module handles PDF text extraction and search functionality.
"""

import os
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any, Optional
from pathlib import Path

class PDFProcessor:
    def __init__(self, pdf_path: str):
        """Initialize PDF processor with a PDF file."""
        self.pdf_path = pdf_path
        self.text_content = ""
        self.pages = []
        self.loaded = False
        
    def load_pdf(self) -> bool:
        """Load and extract text from the PDF."""
        try:
            if not os.path.exists(self.pdf_path):
                return False
                
            pdf_document = fitz.open(self.pdf_path)
            self.pages = []
            
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text()
                self.pages.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'word_count': len(text.split())
                })
                self.text_content += f"\n--- Page {page_num + 1} ---\n{text}\n"
            
            pdf_document.close()
            self.loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def search_text(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Search for text in the PDF and return relevant sections."""
        if not self.loaded:
            if not self.load_pdf():
                return []
        
        query = query if case_sensitive else query.lower()
        results = []
        
        for page in self.pages:
            page_text = page['text'] if case_sensitive else page['text'].lower()
            
            if query in page_text:
                # Find all occurrences
                start = 0
                while True:
                    pos = page_text.find(query, start)
                    if pos == -1:
                        break
                    
                    # Extract context around the match
                    context_start = max(0, pos - 100)
                    context_end = min(len(page['text']), pos + len(query) + 100)
                    context = page['text'][context_start:context_end]
                    
                    results.append({
                        'page_number': page['page_number'],
                        'context': context,
                        'position': pos,
                        'query': query
                    })
                    
                    start = pos + 1
        
        return results
    
    def get_page_content(self, page_number: int) -> Optional[str]:
        """Get content of a specific page."""
        if not self.loaded:
            if not self.load_pdf():
                return None
        
        for page in self.pages:
            if page['page_number'] == page_number:
                return page['text']
        
        return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the PDF content."""
        if not self.loaded:
            if not self.load_pdf():
                return {}
        
        total_words = sum(page['word_count'] for page in self.pages)
        
        return {
            'total_pages': len(self.pages),
            'total_words': total_words,
            'file_name': os.path.basename(self.pdf_path),
            'file_size': os.path.getsize(self.pdf_path) if os.path.exists(self.pdf_path) else 0
        }
    
    def extract_key_sections(self, keywords: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract sections containing specific keywords."""
        if not self.loaded:
            if not self.load_pdf():
                return {}
        
        sections = {}
        
        for keyword in keywords:
            sections[keyword] = []
            
            for page in self.pages:
                if keyword.lower() in page['text'].lower():
                    # Find sentences containing the keyword
                    sentences = re.split(r'[.!?]+', page['text'])
                    
                    for sentence in sentences:
                        if keyword.lower() in sentence.lower():
                            sections[keyword].append({
                                'page_number': page['page_number'],
                                'sentence': sentence.strip(),
                                'keyword': keyword
                            })
        
        return sections

# Global PDF processor instance
pdf_processor: Optional[PDFProcessor] = None

def initialize_pdf(pdf_path: str) -> bool:
    """Initialize the global PDF processor."""
    global pdf_processor
    pdf_processor = PDFProcessor(pdf_path)
    return pdf_processor.load_pdf()

def get_pdf_processor() -> Optional[PDFProcessor]:
    """Get the global PDF processor instance."""
    return pdf_processor
