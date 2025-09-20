import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
import tempfile
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json
import time

# Load environment variables
load_dotenv()

class SmartDocAnalyzer:
    """SmartDoc AI Agent - Document Analyzer"""

    def __init__(self, api_key: str = None):
        """Initialize the analyzer"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or st.session_state.get("api_key", "")
        self.is_configured = False
        self.model = None
        self.last_request_time = 0
        self.rate_limit_delay = 6  # Free tier rate limiting

        if self.api_key:
            self.setup_api()

    def setup_api(self):
        """Setup Gemini API with comprehensive error handling"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

            # Test connection with detailed feedback
            test_response = self.model.generate_content("Test connection")

            if test_response and test_response.text:
                self.is_configured = True
                st.success("✅ Gemini API configured successfully!")
                return True
            else:
                st.error("❌ API test failed")
                return False

        except Exception as e:
            self.handle_api_error(e)
            return False

    def handle_api_error(self, error):
        """Handle API errors with specific messages"""
        error_msg = str(error)
        self.is_configured = False

        if "INVALID_ARGUMENT" in error_msg or "invalid" in error_msg.lower():
            st.error("🔑 **Invalid API Key**")
            st.info("💡 Get a valid key from: https://aistudio.google.com/app/apikey")
        elif "PERMISSION_DENIED" in error_msg:
            st.error("🚫 **Permission Denied** - Check API key permissions")
        elif "quota" in error_msg.lower() or "429" in error_msg:
            st.error("🚫 **Quota Exceeded** - Free tier limit reached")
            st.info("⏰ Try again tomorrow or upgrade to paid tier")
        elif "RESOURCE_EXHAUSTED" in error_msg:
            st.error("🚫 **Resource Exhausted** - Too many requests")
        else:
            st.error(f"❌ **API Error**: {error_msg}")

    def rate_limit_protection(self):
        """Smart rate limiting for free tier"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit_delay:
            wait_time = self.rate_limit_delay - time_since_last
            progress_bar = st.progress(0)
            for i in range(int(wait_time * 10)):
                progress_bar.progress((i + 1) / (wait_time * 10))
                time.sleep(0.1)
            progress_bar.empty()

        self.last_request_time = time.time()

    def validate_pdf_file(self, uploaded_file) -> Tuple[bool, str]:
        """PDF validation"""
        if not uploaded_file:
            return False, "No file uploaded"

        if not uploaded_file.name.lower().endswith('.pdf'):
            return False, "File must be a PDF (.pdf extension)"

        if uploaded_file.size > 10 * 1024 * 1024:
            return False, f"File too large: {self.format_file_size(uploaded_file.size)}. Max: 10MB"

        if uploaded_file.size < 1024:  # Less than 1KB
            return False, "File appears to be too small or corrupted"

        return True, ""

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 ** 2):.1f} MB"

    def extract_text_from_pdf(self, uploaded_file) -> Tuple[str, dict]:
        """PDF text extraction with detailed metadata"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                uploaded_file.seek(0)
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            text = ""
            metadata = {
                'file_name': uploaded_file.name,
                'file_size': uploaded_file.size,
                'extraction_time': datetime.now().isoformat(),
                'file_hash': hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]
            }

            with open(tmp_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Extract metadata
                metadata['total_pages'] = len(pdf_reader.pages)

                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', 'Unknown'),
                        'author': pdf_reader.metadata.get('/Author', 'Unknown'),
                        'subject': pdf_reader.metadata.get('/Subject', 'Unknown'),
                        'creator': pdf_reader.metadata.get('/Creator', 'Unknown'),
                        'creation_date': str(pdf_reader.metadata.get('/CreationDate', 'Unknown'))
                    })

                # Extract text (enhanced with page tracking)
                max_pages = min(5, len(pdf_reader.pages))  # Free tier limit
                metadata['processed_pages'] = max_pages
                pages_with_content = 0

                for page_num in range(max_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()

                        if page_text.strip():
                            text += f"\n\n=== PAGE {page_num + 1} ===\n"
                            text += page_text.strip()
                            pages_with_content += 1
                    except Exception as page_error:
                        st.warning(f"⚠️ Could not extract text from page {page_num + 1}: {str(page_error)}")

                metadata['pages_with_content'] = pages_with_content

            # Clean up
            os.unlink(tmp_file_path)

            # Text processing
            if len(text) > 12000:  
                text = text[:12000] + "\n\n[Content truncated for API optimization...]"
                metadata['content_truncated'] = True
            else:
                metadata['content_truncated'] = False

            metadata['final_text_length'] = len(text)
            metadata['word_count'] = len(text.split())

            return text, metadata

        except Exception as e:
            st.error(f"❌ PDF extraction error: {str(e)}")
            return "", {'error': str(e)}

    def analyze_document(self, text: str, analysis_type: str = "comprehensive", 
                        custom_query: str = "", include_metadata: bool = True) -> str:
        """document analysis with multiple modes"""

        if not self.is_configured or not self.model:
            return "❌ API not configured properly. Please check your API key."

        if not text or len(text.strip()) < 20:
            return "❌ Insufficient text content for analysis."

        # Rate limiting
        self.rate_limit_protection()

        try:
            # prompts for different analysis types
            prompts = {
                "summary": f"""
                Create a comprehensive summary of this document:

                **Requirements:**
                - Executive summary (2-3 sentences)
                - Main topics covered
                - Key findings or conclusions
                - Important details or statistics
                - Overall assessment

                **Document Content:**
                {text}

                **Format:** Use clear headers and bullet points for readability.
                """,

                "comprehensive": f"""
                Perform a thorough analysis of this document:

                **Analysis Framework:**
                1. **Document Overview** - Purpose, scope, and context
                2. **Key Themes & Topics** - Main subjects discussed
                3. **Critical Findings** - Important discoveries or insights
                4. **Data & Evidence** - Statistics, facts, and supporting information
                5. **Arguments & Positions** - Main claims and reasoning
                6. **Implications** - What this means and why it matters
                7. **Recommendations** - Suggested actions or next steps
                8. **Assessment** - Overall evaluation and significance

                **Document Content:**
                {text}

                **Instructions:** Provide detailed analysis under each section with specific examples from the text.
                """,

                "insights": f"""
                Extract and analyze key insights from this document:

                **Focus Areas:**
                • **Top 5 Most Important Findings** - What are the critical discoveries?
                • **Trends & Patterns** - What patterns emerge from the data/content?
                • **Implications & Impact** - What are the broader consequences?
                • **Opportunities & Challenges** - What possibilities and obstacles are identified?
                • **Strategic Recommendations** - What actions should be taken?

                **Document Content:**
                {text}

                **Format:** Use clear categories with bullet points and explanations.
                """,

                "technical": f"""
                Provide a technical analysis of this document:

                **Technical Framework:**
                - **Methodology** - Approaches, techniques, or processes used
                - **Technical Details** - Specifications, parameters, or technical aspects
                - **Data Analysis** - Statistical information and data interpretation
                - **Technical Conclusions** - Engineering, scientific, or technical findings
                - **Implementation Notes** - Practical application considerations

                **Document Content:**
                {text}
                """,

                "custom": f"""
                Based on the document provided, answer this specific question with detailed analysis:

                **Question:** {custom_query}

                **Requirements:**
                - Provide a direct answer to the question
                - Include supporting evidence from the document
                - Explain the context and background
                - Discuss implications or significance
                - Note any limitations or caveats

                **Document Content:**
                {text}

                **Instructions:** Base your answer entirely on the document content and be specific about sources.
                """
            }

            # Select and execute prompt
            if analysis_type == "custom" and custom_query:
                prompt = prompts["custom"]
            else:
                prompt = prompts.get(analysis_type, prompts["comprehensive"])

            # API call with error handling
            with st.spinner(f"🤖 Performing {analysis_type} analysis..."):
                response = self.model.generate_content(prompt)

                if response and response.text:
                    result = response.text

                    # Add metadata footer if requested
                    if include_metadata:
                        result += f"\n\n---\n*Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

                    return result
                else:
                    return "❌ No response generated. The API returned an empty response."

        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg:
                return "🚫 **Quota Exceeded**: Free tier daily limit reached. Try again tomorrow or upgrade to paid tier."
            elif "invalid" in error_msg.lower():
                return "🔑 **Invalid Request**: Please check your API key and try again."
            elif "RESOURCE_EXHAUSTED" in error_msg:
                return "🚫 **Resource Exhausted**: Too many requests. Please wait and try again."
            else:
                return f"❌ **Analysis Error**: {error_msg}"

    def batch_analyze(self, files_data: List[Dict], analysis_type: str = "summary") -> Dict[str, str]:
        """Analyze multiple documents"""
        results = {}
        total_files = len(files_data)

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, file_data in enumerate(files_data):
            file_name = file_data['name']
            text = file_data.get('text', '')

            status_text.text(f"🔍 Analyzing {file_name} ({i+1}/{total_files})")
            progress_bar.progress((i + 1) / total_files)

            if text:
                result = self.analyze_document(text, analysis_type, include_metadata=False)
                results[file_name] = result
            else:
                results[file_name] = "❌ No text content available"

            # Add delay between analyses
            if i < total_files - 1:
                time.sleep(2)

        progress_bar.empty()
        status_text.empty()
        return results

def create_sidebar():
    """sidebar with more options"""
    with st.sidebar:
        st.header("🔧 Configuration")

        # API Key section
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            placeholder="Enter your API key...",
            help="Get your free API key from Google AI Studio"
        )

        if api_key != st.session_state.get("api_key", ""):
            st.session_state.api_key = api_key

        # API Key validation
        if api_key:
            if len(api_key) < 20:
                st.warning("⚠️ API key appears too short")
            else:
                st.success("✅ API key format looks correct")
        else:
            st.error("❌ No API key provided")

            with st.expander("🆓 Get FREE API Key", expanded=True):
                st.markdown("""
                **Completely Free - No Payment Required!**

                1. **Visit**: [Google AI Studio](https://aistudio.google.com/app/apikey)
                2. **Sign in** with Google account
                3. **Click** "Create API Key"
                4. **Select** project (or create new)
                5. **Copy** generated key
                6. **Paste** above

                **Free Tier Includes:**
                - 250 requests per day
                - 10 requests per minute
                - All analysis modes
                """)

        st.markdown("---")

        # Analysis Settings
        st.header("⚙️ Analysis Settings")

        analysis_mode = st.selectbox(
            "Analysis Mode",
            ["comprehensive", "summary", "insights", "technical", "custom"],
            format_func=lambda x: {
                "comprehensive": "📊 Comprehensive Analysis",
                "summary": "📝 Smart Summary",
                "insights": "💡 Key Insights",
                "technical": "🔬 Technical Analysis",
                "custom": "❓ Custom Question"
            }[x],
            help="Choose the type of analysis to perform"
        )

        custom_query = ""
        if analysis_mode == "custom":
            custom_query = st.text_area(
                "Your Question",
                placeholder="Ask a specific question about the document...",
                height=120,
                help="Be specific for better results"
            )

        st.session_state.analysis_mode = analysis_mode
        st.session_state.custom_query = custom_query

        # Processing Options
        st.markdown("---")
        st.header("⚙️ Processing Options")

        include_metadata = st.checkbox("Include analysis metadata", value=True)
        st.session_state.include_metadata = include_metadata

        max_pages = st.slider("Max pages to process", 1, 5, 5, help="Free tier limit: 5 pages")
        st.session_state.max_pages = max_pages

        st.markdown("---")

        # Statistics
        if 'processed_files' in st.session_state and st.session_state.processed_files:
            st.header("📊 Session Statistics")
            files = st.session_state.processed_files

            total_files = len(files)
            total_pages = sum(f.get('metadata', {}).get('processed_pages', 0) for f in files)
            total_words = sum(f.get('metadata', {}).get('word_count', 0) for f in files)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Files", total_files)
                st.metric("Pages", total_pages)
            with col2:
                st.metric("Words", f"{total_words:,}")
                if 'analysis_count' in st.session_state:
                    st.metric("Analyses", st.session_state.analysis_count)

        st.markdown("---")

        # Usage Info
        st.header("🆓 Free Tier Limits")
        st.info("""
        **Daily Limits:**
        • 250 API requests
        • 10 requests per minute
        • First 5 pages per PDF
        • 12,000 characters per analysis

        **Features Included:**
        • All analysis modes
        • Multi-document support
        • Interactive chat
        • Export results
        """)

        # Tips
        st.markdown("---")
        st.header("💡 Pro Tips")
        st.markdown("""
        • **Upload quality PDFs** for better text extraction
        • **Use specific questions** in custom mode
        • **Try different analysis modes** for various perspectives
        • **Check document metadata** for processing details
        """)

def main():
    """main application"""
    st.set_page_config(
        page_title="SmartDoc AI Agent",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0

    # Header
    st.title("📚 SmartDoc AI Agent")
    st.markdown("**Advanced Document Analyzer powered by Google Gemini Pro (REVISED VERSION)**")

    # Create sidebar
    create_sidebar()

    # Check API key
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar to continue.")
        return

    # Initialize analyzer
    if 'analyzer' not in st.session_state or st.session_state.get('current_key') != api_key:
        with st.spinner("🔧 Initializing SmartDoc AI Agent..."):
            st.session_state.analyzer = SmartDocAnalyzer(api_key)
            st.session_state.current_key = api_key

    analyzer = st.session_state.analyzer

    if not analyzer.is_configured:
        st.error("❌ Failed to configure Gemini API. Please check your API key and try again.")
        return

    # Main interface
    st.header("📄 Document Processing")

    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files for analysis (max 10MB each)"
    )

    if uploaded_files:
        # File validation and info
        valid_files = []

        with st.expander(f"📋 File Validation ({len(uploaded_files)} files)", expanded=True):
            for i, file in enumerate(uploaded_files):
                is_valid, error_msg = analyzer.validate_pdf_file(file)

                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                with col1:
                    st.write(f"📄 **{file.name}**")
                with col2:
                    st.write(f"Size: {analyzer.format_file_size(file.size)}")
                with col3:
                    st.write(f"Hash: {hashlib.md5(file.getvalue()).hexdigest()[:8]}")
                with col4:
                    if is_valid:
                        st.success("✅")
                        valid_files.append(file)
                    else:
                        st.error("❌")
                        st.caption(error_msg)

        if valid_files:
            st.success(f"✅ {len(valid_files)} files ready for processing")

            # Processing options
            col1, col2, col3 = st.columns([2, 2, 2])

            with col1:
                process_button = st.button("🔄 Process Documents", type="primary")
            with col2:
                if st.session_state.processed_files:
                    batch_analyze_button = st.button("📊 Batch Analyze", type="secondary")
                else:
                    batch_analyze_button = False
            with col3:
                if st.session_state.processed_files:
                    clear_button = st.button("🗑️ Clear Session")
                    if clear_button:
                        st.session_state.processed_files = []
                        st.session_state.chat_history = []
                        st.session_state.analysis_count = 0
                        st.rerun()

            # Process documents
            if process_button:
                process_documents(analyzer, valid_files)

            # Batch analyze
            if batch_analyze_button:
                perform_batch_analysis(analyzer)

    # Show processed documents
    if st.session_state.processed_files:
        show_processed_documents(analyzer)

    # Chat interface
    if st.session_state.processed_files:
        show_chat_interface(analyzer)

def process_documents(analyzer, uploaded_files):
    """Process uploaded documents with progress tracking"""
    st.header("🔄 Processing Documents")

    processed_files = []

    # Overall progress
    overall_progress = st.progress(0)
    status_text = st.empty()

    for i, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name} ({i+1}/{len(uploaded_files)})")
        overall_progress.progress((i + 1) / len(uploaded_files))

        # Extract text
        with st.spinner(f"📖 Extracting text from {file.name}..."):
            text, metadata = analyzer.extract_text_from_pdf(file)

        if text:
            processed_files.append({
                'name': file.name,
                'text': text,
                'metadata': metadata,
                'processed_at': datetime.now().isoformat()
            })

            st.success(f"✅ Processed {file.name} - {metadata.get('processed_pages', 0)} pages, {metadata.get('word_count', 0)} words")
        else:
            st.error(f"❌ Failed to process {file.name}")

    overall_progress.empty()
    status_text.empty()

    if processed_files:
        st.session_state.processed_files.extend(processed_files)
        st.success(f"🎉 Successfully processed {len(processed_files)} documents!")

def show_processed_documents(analyzer):
    """Display processed documents with analysis options"""
    st.header(f"📚 Processed Documents ({len(st.session_state.processed_files)})")

    for i, file_data in enumerate(st.session_state.processed_files):
        with st.expander(f"📄 {file_data['name']}", expanded=False):

            # Document info
            metadata = file_data.get('metadata', {})

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pages", metadata.get('processed_pages', 'Unknown'))
            with col2:
                st.metric("Words", metadata.get('word_count', 'Unknown'))
            with col3:
                st.metric("Size", metadata.get('file_size', 'Unknown'))

            # Quick analysis
            if st.button(f"🔍 Analyze {file_data['name']}", key=f"analyze_{i}"):
                analysis_mode = st.session_state.get('analysis_mode', 'comprehensive')
                custom_query = st.session_state.get('custom_query', '')

                result = analyzer.analyze_document(
                    file_data['text'],
                    analysis_mode,
                    custom_query,
                    st.session_state.get('include_metadata', True)
                )

                st.session_state.analysis_count += 1

                st.subheader(f"Analysis Results - {file_data['name']}")
                st.write(result)

def perform_batch_analysis(analyzer):
    """Perform batch analysis on all processed documents"""
    st.header("📊 Batch Analysis Results")

    analysis_mode = st.session_state.get('analysis_mode', 'summary')

    if analysis_mode == 'custom':
        custom_query = st.session_state.get('custom_query', '')
        if not custom_query:
            st.warning("⚠️ Please enter a custom question in the sidebar for batch analysis.")
            return

    results = analyzer.batch_analyze(st.session_state.processed_files, analysis_mode)
    st.session_state.analysis_count += len(results)

    for filename, result in results.items():
        st.subheader(f"📄 {filename}")
        st.write(result)
        st.markdown("---")

def show_chat_interface(analyzer):
    """Interactive chat interface for processed documents"""
    st.header("💬 Interactive Document Chat")

    # Chat input
    user_question = st.text_input(
        "Ask a question about your documents:",
        placeholder="e.g., What are the main conclusions across all documents?",
        key="chat_input"
    )

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        ask_button = st.button("🔍 Ask Question", type="primary")
    with col2:
        if st.session_state.chat_history:
            if st.button("🧹 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
    with col3:
        if st.session_state.processed_files and st.button("📋 Document Summary"):
            # Generate summary of all documents
            combined_text = "\n\n---DOCUMENT SEPARATOR---\n\n".join([
                f"DOCUMENT: {f['name']}\n{f['text']}" 
                for f in st.session_state.processed_files
            ])

            summary = analyzer.analyze_document(
                combined_text[:8000],  # Limit for API
                "summary",
                include_metadata=False
            )

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"**📋 Multi-Document Summary:**\n\n{summary}",
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()

    # Process question
    if ask_button and user_question:
        # Add user question to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question,
            "timestamp": datetime.now().isoformat()
        })

        # Get answer from first document (can be enhanced for multi-doc search)
        if st.session_state.processed_files:
            first_doc = st.session_state.processed_files[0]

            answer = analyzer.analyze_document(
                first_doc['text'],
                "custom",
                user_question,
                include_metadata=False
            )

            st.session_state.analysis_count += 1

            # Add answer to chat
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": answer,
                "timestamp": datetime.now().isoformat()
            })

        st.rerun()

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation History")

        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
                    st.caption(f"Asked at {message['timestamp'][:19]}")
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    st.caption(f"Answered at {message['timestamp'][:19]}")

if __name__ == "__main__":
    main()
