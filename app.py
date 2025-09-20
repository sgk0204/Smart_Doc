import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
import tempfile
import time
from typing import List, Dict, Tuple
from datetime import datetime

# Load environment variables
load_dotenv()

class SmartDocAnalyzer:
    """SmartDoc AI Agent - Document Analyzer using Google Gemini Pro """

    def __init__(self, api_key: str = None):
        """Initialize the analyzer with proper API configuration"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or st.session_state.get("api_key", "")
        self.is_configured = False
        self.model = None
        self.last_request_time = 0
        self.rate_limit_delay = 6  

        if self.api_key:
            self.setup_api()

    def setup_api(self):
        """Setup Gemini API with proper error handling"""
        try:
            # Configure API key
            genai.configure(api_key=self.api_key)

            # Initialize model - CORRECT METHOD
            self.model = genai.GenerativeModel('gemini-1.5-flash')

            # Test connection
            with st.spinner("🔧 Testing API connection..."):
                test_response = self.model.generate_content("Hello, this is a test.")

                if test_response and test_response.text:
                    self.is_configured = True
                    st.success("✅ Gemini API configured successfully!")
                    return True
                else:
                    st.error("❌ API test failed - no response received")
                    return False

        except Exception as e:
            error_msg = str(e)
            self.is_configured = False

            # Provide specific error messages
            if "INVALID_ARGUMENT" in error_msg or "invalid" in error_msg.lower():
                st.error("🔑 **Invalid API Key** - Please check your Gemini API key")
                st.info("💡 Get a valid key from: https://aistudio.google.com/app/apikey")
            elif "PERMISSION_DENIED" in error_msg:
                st.error("🚫 **Permission Denied** - API key lacks required permissions")
            elif "quota" in error_msg.lower() or "429" in error_msg:
                st.error("🚫 **Quota Exceeded** - Free tier limit reached")
                st.info("⏰ Try again tomorrow or upgrade to paid tier")
            else:
                st.error(f"❌ **API Configuration Failed**: {error_msg}")

            return False

    def rate_limit_protection(self):
        """Implement rate limiting for free tier"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit_delay:
            wait_time = self.rate_limit_delay - time_since_last
            with st.spinner(f"⏳ Rate limiting: waiting {wait_time:.1f}s..."):
                time.sleep(wait_time)

        self.last_request_time = time.time()

    def validate_pdf_file(self, uploaded_file) -> Tuple[bool, str]:
        """Validate uploaded PDF file"""
        if not uploaded_file:
            return False, "No file uploaded"

        if not uploaded_file.name.lower().endswith('.pdf'):
            return False, "File must be a PDF"

        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB limit
            return False, "File size must be less than 10MB"

        return True, ""

    def extract_text_from_pdf(self, uploaded_file) -> Tuple[str, dict]:
        """Extract text from PDF with metadata"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                uploaded_file.seek(0)
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # Extract text and metadata
            text = ""
            metadata = {}

            with open(tmp_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Get metadata
                metadata['total_pages'] = len(pdf_reader.pages)
                if pdf_reader.metadata:
                    metadata['title'] = pdf_reader.metadata.get('/Title', 'Unknown')
                    metadata['author'] = pdf_reader.metadata.get('/Author', 'Unknown')

                # Extract text (limit to first 5 pages for free tier)
                max_pages = min(5, len(pdf_reader.pages))
                metadata['processed_pages'] = max_pages

                for page_num in range(max_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()

                    if page_text.strip():
                        text += f"\n\n--- Page {page_num + 1} ---\n"
                        text += page_text.strip()

            # Clean up temporary file
            os.unlink(tmp_file_path)

            # Limit text length for API efficiency
            if len(text) > 8000:
                text = text[:8000] + "\n\n[Content truncated for free tier optimization...]"

            metadata['text_length'] = len(text)
            metadata['extraction_time'] = datetime.now().isoformat()

            return text, metadata

        except Exception as e:
            st.error(f"❌ Error extracting text from PDF: {str(e)}")
            return "", {}

    def analyze_document(self, text: str, analysis_type: str = "summary", custom_query: str = "") -> str:
        """Analyze document text using Gemini Pro"""
        if not self.is_configured or not self.model:
            return "❌ API not configured. Please check your API key."

        if not text or len(text.strip()) < 10:
            return "❌ No valid text content found in the document."

        # Apply rate limiting
        self.rate_limit_protection()

        try:
            # Define analysis prompts
            prompts = {
                "summary": f"""
                Provide a concise summary of this document in 200 words or less:

                {text}

                Include:
                - Main topic/purpose
                - Key findings or points
                - Important conclusions
                """,

                "comprehensive": f"""
                Analyze this document thoroughly and provide:

                1. **Executive Summary** (2-3 sentences)
                2. **Key Topics & Themes**
                3. **Important Facts & Figures**
                4. **Main Arguments/Conclusions**
                5. **Recommendations** (if applicable)

                Document:
                {text}
                """,

                "insights": f"""
                Extract the key insights from this document:

                • What are the 5 most important findings?
                • What trends or patterns are identified?
                • What are the implications?
                • What recommendations are made?

                Document:
                {text}
                """,

                "custom": f"""
                Based on this document, answer the following question:

                **Question:** {custom_query}

                **Document:**
                {text}

                **Instructions:** Provide a detailed answer with supporting evidence from the document.
                """
            }

            # Select appropriate prompt
            if analysis_type == "custom" and custom_query:
                prompt = prompts["custom"]
            else:
                prompt = prompts.get(analysis_type, prompts["summary"])

            # Make API call
            with st.spinner("🤖 Analyzing document with Gemini..."):
                response = self.model.generate_content(prompt)

                if response and response.text:
                    return response.text
                else:
                    return "❌ No response generated. Please try again."

        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return "🚫 Free tier quota exceeded. Please try again tomorrow."
            elif "invalid" in error_msg.lower():
                return "🔑 Invalid API key. Please check your configuration."
            else:
                return f"❌ Analysis error: {error_msg}"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 ** 2):.1f} MB"

def main():
    """Main application function"""
    st.set_page_config(
        page_title="SmartDoc AI Agent (REVISED)",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 SmartDoc AI Agent")
    st.markdown("**Intelligent Document Analyzer **")

    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 API Configuration")

        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            placeholder="Enter your API key..."
        )

        if api_key != st.session_state.get("api_key", ""):
            st.session_state.api_key = api_key

        if not api_key:
            st.warning("⚠️ Please enter your API key")
            with st.expander("🆓 Get FREE API Key"):
                st.markdown("""
                **100% Free - No Payment Required!**

                1. Visit: [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. Sign in with Google account
                3. Click "Create API Key"
                4. Copy and paste here
                """)
            return

        # Analysis options
        st.markdown("---")
        st.header("📊 Analysis Options")

        analysis_type = st.selectbox(
            "Analysis Type",
            ["summary", "comprehensive", "insights", "custom"],
            format_func=lambda x: {
                "summary": "📝 Quick Summary",
                "comprehensive": "📊 Comprehensive Analysis",
                "insights": "💡 Key Insights",
                "custom": "❓ Custom Question"
            }[x]
        )

        custom_query = ""
        if analysis_type == "custom":
            custom_query = st.text_area(
                "Your Question",
                placeholder="Ask a specific question about the document...",
                height=100
            )

        st.session_state.analysis_type = analysis_type
        st.session_state.custom_query = custom_query

        st.markdown("---")
        st.header("🆓 Free Tier Info")
        st.info("""
        **Daily Limits:**
        • 250 requests per day
        • First 5 pages of PDF
        • 8,000 character limit
        • 10 requests per minute
        """)

    # Initialize analyzer
    if api_key:
        if 'analyzer' not in st.session_state or st.session_state.get('current_api_key') != api_key:
            st.session_state.analyzer = SmartDocAnalyzer(api_key)
            st.session_state.current_api_key = api_key

        analyzer = st.session_state.analyzer

        if not analyzer.is_configured:
            st.error("❌ API configuration failed. Please check your API key.")
            return
    else:
        return

    # Main interface
    st.header("📄 Document Upload")

    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=['pdf'],
        help="Upload a PDF document for analysis (max 10MB, first 5 pages)"
    )

    if uploaded_file:
        # Validate file
        is_valid, error_msg = analyzer.validate_pdf_file(uploaded_file)

        if not is_valid:
            st.error(f"❌ {error_msg}")
            return

        # Show file info
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📄 **File:** {uploaded_file.name}")
        with col2:
            st.info(f"📊 **Size:** {format_file_size(uploaded_file.size)}")

        # Analysis button
        if st.button("🔍 Analyze Document", type="primary"):

            # Extract text
            with st.spinner("📖 Extracting text from PDF..."):
                text, metadata = analyzer.extract_text_from_pdf(uploaded_file)

            if not text:
                st.error("❌ Could not extract text from the PDF")
                return

            # Show extraction info
            st.success(f"✅ Extracted text from {metadata.get('processed_pages', 'unknown')} pages")

            if metadata.get('total_pages', 0) > 5:
                st.warning(f"⚠️ PDF has {metadata['total_pages']} pages, analyzed first 5 (free tier limit)")

            # Show metadata
            with st.expander("📋 Document Information"):
                st.json(metadata)

            # Perform analysis
            st.header("🔍 Analysis Results")

            analysis_type = st.session_state.get('analysis_type', 'summary')
            custom_query = st.session_state.get('custom_query', '')

            result = analyzer.analyze_document(text, analysis_type, custom_query)
            st.write(result)

            # Store results for potential chat
            st.session_state.document_text = text
            st.session_state.analysis_complete = True

    # Simple chat interface
    if st.session_state.get('analysis_complete') and 'document_text' in st.session_state:
        st.markdown("---")
        st.header("💬 Ask Follow-up Questions")

        follow_up_question = st.text_input(
            "Ask a question about the document:",
            placeholder="e.g., What are the main conclusions?"
        )

        if st.button("🔍 Ask") and follow_up_question:
            answer = analyzer.analyze_document(
                st.session_state.document_text, 
                "custom", 
                follow_up_question
            )
            st.write("**Answer:**")
            st.write(answer)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        🤖 SmartDoc AI Agent
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
