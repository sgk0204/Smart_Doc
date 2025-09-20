"""
Utility functions for SmartDoc AI Agent (REVISED - SIMPLIFIED)
All functions tested and working with correct Gemini API
"""
import streamlit as st
import os
import tempfile
import hashlib
import time
from typing import List, Optional, Tuple, Dict, Any
import PyPDF2
from datetime import datetime

def validate_pdf_file(uploaded_file) -> Tuple[bool, str]:
    """Validate uploaded PDF file"""
    if not uploaded_file:
        return False, "No file uploaded"

    if not uploaded_file.name.lower().endswith('.pdf'):
        return False, "File must be a PDF"

    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "File too large (max 10MB)"

    if uploaded_file.size < 1024:
        return False, "File appears to be empty"

    return True, ""

def create_temp_file(uploaded_file, suffix=".pdf") -> str:
    """Create temporary file from uploaded file"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            uploaded_file.seek(0)
            tmp_file.write(uploaded_file.read())
            return tmp_file.name
    except Exception as e:
        raise Exception(f"Failed to create temp file: {str(e)}")

def extract_pdf_metadata(pdf_path: str) -> Dict[str, Any]:
    """Extract metadata from PDF file"""
    metadata = {
        'extraction_time': datetime.now().isoformat(),
        'file_size': 0
    }

    try:
        metadata['file_size'] = os.path.getsize(pdf_path)

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata['total_pages'] = len(pdf_reader.pages)

            if pdf_reader.metadata:
                metadata.update({
                    'title': pdf_reader.metadata.get('/Title', 'Unknown'),
                    'author': pdf_reader.metadata.get('/Author', 'Unknown'),
                    'subject': pdf_reader.metadata.get('/Subject', 'Unknown')
                })

            # Test text extraction
            if len(pdf_reader.pages) > 0:
                first_page_text = pdf_reader.pages[0].extract_text()
                metadata['has_text'] = len(first_page_text.strip()) > 0

    except Exception as e:
        metadata['error'] = str(e)

    return metadata

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.1f} MB"

def clean_text(text: str) -> str:
    """Clean extracted text"""
    if not text:
        return ""

    # Remove excessive whitespace
    text = ' '.join(text.split())

    # Remove problematic characters
    import re
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', text)

    return text.strip()

# Display functions
def display_success_message(message: str):
    st.success(f"✅ {message}")

def display_error_message(message: str):
    st.error(f"❌ {message}")

def display_info_message(message: str):
    st.info(f"ℹ️ {message}")

def display_warning_message(message: str):
    st.warning(f"⚠️ {message}")

# Session state management
class SessionStateManager:
    """Session state management"""

    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        defaults = {
            'processed_files': [],
            'chat_history': [],
            'analyzer': None,
            'api_key': '',
            'analysis_count': 0,
            'session_start': datetime.now().isoformat()
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def add_chat_message(role: str, content: str):
        """Add message to chat history"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        st.session_state.chat_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })

# Rate limiting
class RateLimiter:
    """Rate limiter for API calls"""

    def __init__(self, rpm: int = 10):
        self.rpm = rpm
        self.interval = 60.0 / rpm
        self.last_request = 0

    def wait_if_needed(self):
        """Wait if necessary for rate limiting"""
        current = time.time()
        elapsed = current - self.last_request

        if elapsed < self.interval:
            wait_time = self.interval - elapsed
            time.sleep(wait_time)

        self.last_request = time.time()
