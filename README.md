# 📚 SmartDoc AI Agent

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini-blue.svg)](https://ai.google.dev/)

**An intelligent Document Analyzer powered by Google Gemini Pro**

Transform your PDF documents into an interactive knowledge base with AI-powered insights, summaries, and question-answering capabilities.

## 🌟 Features

### Core Functionality
- **📄 Multi-Document Support**: Upload and analyze multiple PDF files simultaneously
- **🔍 Intelligent Analysis**: Four different analysis modes powered by Gemini Pro
- **💬 Interactive Chat**: Ask questions about your documents and get instant answers
- **📊 Document Insights**: Extract metadata, key findings, and comprehensive summaries
- **🔒 Secure Processing**: Local processing with secure API key handling

### Analysis Modes
1. **Comprehensive Analysis**: Complete document breakdown with executive summary, key topics, facts, and recommendations
2. **Quick Summary**: Concise overview focusing on main points and conclusions
3. **Key Insights**: Extract trends, patterns, and important discoveries
4. **Custom Query**: Ask specific questions and get detailed, contextual answers

### Advanced Features
- **Real-time Processing**: Progress indicators and status updates
- **File Validation**: Automatic validation of file types and sizes
- **Metadata Extraction**: Document properties, page count, and content statistics
- **Chat History**: Persistent conversation history within sessions
- **Error Handling**: Comprehensive error management and user feedback
- **Responsive UI**: Clean, professional interface with expandable sections

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd SmartDoc_AI_Agent

   # Or download and extract the ZIP file
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the environment template
   cp .env.example .env

   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   # Basic version
   streamlit run app.py

   # Enhanced version (recommended)
   streamlit run app_enhanced.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Enter your API key in the sidebar
   - Upload PDF documents and start analyzing!

## 📖 How to Use

### Step 1: Configuration
1. Enter your Gemini API key in the sidebar
2. Choose your preferred analysis mode
3. Optionally enter a custom question for targeted analysis

### Step 2: Upload Documents
1. Click "Browse files" and select PDF documents (max 10MB each)
2. Review file validation results
3. Proceed with valid files only

### Step 3: Analysis
1. Click "Analyze Documents" to process your files
2. Review document metadata and statistics
3. Read the comprehensive analysis results

### Step 4: Interactive Chat
1. Use the chat interface to ask follow-up questions
2. Get instant, contextual answers based on your documents
3. Build upon previous conversations within the session

## 🏗️ Architecture

### System Components
```
┌─────────────────────┐
│   Streamlit UI      │ ← User Interface Layer
├─────────────────────┤
│  Document Processor │ ← PDF Processing & Text Extraction
├─────────────────────┤
│   Gemini Pro API    │ ← AI Analysis Engine
├─────────────────────┤
│  Session Management │ ← State & History Management
└─────────────────────┘
```

### Key Technologies
- **Frontend**: Streamlit for interactive web interface
- **AI Model**: Google Gemini 2.5 Pro for document analysis
- **PDF Processing**: PyPDF2 for text extraction and metadata
- **State Management**: Streamlit session state for persistence
- **Configuration**: Environment-based settings with validation

### Data Flow
1. **Upload** → PDF files uploaded through Streamlit interface
2. **Validate** → File type, size, and content validation
3. **Process** → Text extraction and metadata collection
4. **Analyze** → AI-powered analysis using Gemini Pro
5. **Present** → Results displayed with interactive chat interface

## 📁 Project Structure

```
SmartDoc_AI_Agent/
├── app.py                 # Basic Streamlit application
├── app_enhanced.py        # Enhanced version with advanced features
├── config.py             # Configuration settings and constants
├── utils.py              # Utility functions and helpers
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (add your API key)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── assets/
    └── architecture_diagram.png
```

### File Descriptions
- **`app.py`**: Basic version of the application with core functionality
- **`app_enhanced.py`**: Production-ready version with advanced features (recommended)
- **`config.py`**: Centralized configuration management
- **`utils.py`**: Helper functions for file processing and UI components
- **`requirements.txt`**: All Python dependencies
- **`.env`**: Environment variables (create from template)

## ⚙️ Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
DEBUG=True
MAX_FILE_SIZE=10MB
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Application Settings
The application can be configured through `config.py`:
- Model selection (default: gemini-2.5-pro)
- File size limits and supported formats
- UI layout and styling options
- Error messages and user feedback

## 🔧 Development

### Running in Development Mode
```bash
# Enable debug mode
export DEBUG=True

# Run with auto-reload
streamlit run app_enhanced.py --runner.headless=true
```

### Adding New Features
1. **New Analysis Types**: Add to `SmartDocAnalyzer.analyze_document_with_gemini()`
2. **File Format Support**: Extend `validate_pdf_file()` in `utils.py`
3. **UI Components**: Add new sections to the main interface functions

### Testing
```bash
# Basic functionality test
python -c "from utils import validate_pdf_file; print('Utils imported successfully')"

# Configuration test  
python -c "from config import Config; print('Config loaded successfully')"
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to a GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select the repository
4. Set `GEMINI_API_KEY` in the secrets management
5. Deploy with `streamlit run app_enhanced.py`

### Local Server
```bash
# Run on specific port
streamlit run app_enhanced.py --server.port 8080

# Run with custom configuration
streamlit run app_enhanced.py --server.headless=true --server.port 8080
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_enhanced.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -am 'Add new feature'`
5. **Push to the branch**: `git push origin feature/new-feature`
6. **Submit a pull request**

### Contribution Guidelines
- Follow Python PEP 8 style guidelines
- Add docstrings to all functions
- Test new features thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**API Key Not Working**
- Verify your API key is correct and active
- Check that you have sufficient API quota
- Ensure the key has appropriate permissions

**File Upload Errors**
- Check file size (must be under 10MB)
- Verify file is a valid PDF
- Try with a different PDF file

**Analysis Failures**
- Check your internet connection
- Verify API key is properly set
- Try with a smaller document first

**Performance Issues**
- Large files may take longer to process
- Consider using Quick Summary mode for faster results
- Check available system memory

### Getting Help
1. Check the troubleshooting section above
2. Review error messages in the application
3. Check the [Gemini API documentation](https://ai.google.dev/gemini-api/docs)
4. Open an issue on GitHub with detailed error information

## 🔗 Useful Links

- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python PDF Processing Guide](https://pypdf2.readthedocs.io/)
- [Get Gemini API Key](https://aistudio.google.com/app/apikey)

## 📊 Performance Notes

- **File Size**: Recommended maximum 10MB per PDF for optimal performance
- **Processing Time**: Varies based on document length and complexity
- **API Limits**: Respect Gemini API rate limits and quotas
- **Memory Usage**: Large documents may require significant memory

## 🎯 Use Cases

### Business & Professional
- **Contract Analysis**: Extract key terms and conditions
- **Report Summarization**: Get quick insights from lengthy reports  
- **Research Papers**: Understand complex academic documents
- **Policy Review**: Analyze compliance and regulatory documents

### Academic & Research
- **Literature Review**: Summarize research papers and articles
- **Thesis Analysis**: Extract key findings from academic work
- **Grant Applications**: Review and analyze funding proposals
- **Course Materials**: Process educational content and textbooks

### Personal & General
- **Legal Documents**: Understand contracts and agreements
- **Manual Processing**: Get insights from user manuals
- **Financial Reports**: Analyze investment and financial documents
- **Healthcare Records**: Review medical reports and documentation

---

**Built with ❤️ using Google Gemini Pro and Streamlit**

For questions, suggestions, or support, please open an issue on GitHub.
