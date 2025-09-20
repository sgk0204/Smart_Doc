# 📚 SmartDoc AI Agent - Complete Documentation

> **🤖 Intelligent Document Analyzer powered by Google Gemini Pro**  
> Transform your PDF documents into actionable insights with AI-powered analysis, interactive chat, and professional-grade features.

---

## 🎯 Overview

**SmartDoc AI Agent** is a sophisticated document analysis platform that leverages Google's Gemini Pro AI to transform PDF documents into comprehensive insights. Whether you're analyzing research papers, business reports, legal documents, or technical manuals, SmartDoc provides intelligent analysis with multiple modes tailored to your specific needs.

### 🌟 What Makes SmartDoc Special?

- **🤖 Advanced AI Analysis**: Powered by Google Gemini Pro for state-of-the-art document understanding
- **🆓 Free Tier Friendly**: Optimized for Gemini's generous free tier (250 requests/day)
- **📱 Professional UI**: Clean, modern interface built with Streamlit
- **💬 Interactive Chat**: Have conversations with your documents
- **📊 Multiple Analysis Modes**: From quick summaries to comprehensive technical analysis
- **🔄 Batch Processing**: Analyze multiple documents simultaneously
- **📈 Session Tracking**: Monitor usage and performance metrics
- **🔧 Production Ready**: Robust error handling and enterprise-grade features

---
## Demo Video
![Demo](Smart_doc_demo - Made with Clipchamp.mp4)

## ✨ Key Features

### 🔍 Document Analysis
- **Multi-Modal Analysis**: 5 different analysis modes for various use cases
- **PDF Text Extraction**: Advanced text extraction with metadata preservation
- **Content Validation**: File format validation and content verification
- **Progress Tracking**: Real-time processing updates and status indicators

### 🤖 AI-Powered Intelligence
- **Comprehensive Analysis**: Detailed document breakdown with key findings
- **Smart Summaries**: Concise overviews highlighting essential information
- **Key Insights Extraction**: Identify patterns, trends, and critical discoveries
- **Technical Analysis**: Specialized analysis for technical and scientific documents
- **Custom Q&A**: Ask specific questions about document content

### 💬 Interactive Features
- **Document Chat**: Have natural conversations with your documents
- **Follow-up Questions**: Ask clarifying questions and get detailed responses
- **Conversation History**: Track your interactions with timestamps
- **Multi-Document Summaries**: Generate combined insights across documents

### 🔧 Professional Tools
- **Batch Processing**: Analyze multiple documents efficiently
- **Session Management**: Persistent state across browser sessions
- **Usage Statistics**: Track files processed, pages analyzed, and API usage
- **Error Recovery**: Comprehensive error handling with helpful messages
- **Rate Limiting**: Smart throttling to respect API limits

### 🆓 Free Tier Optimization
- **Smart Chunking**: Optimized content processing for API efficiency
- **Rate Management**: Automatic pacing to maximize free tier benefits
- **Content Truncation**: Intelligent text limiting without losing context
- **Progress Indicators**: Clear feedback on processing status

---

## 🚀 Quick Start

Get SmartDoc AI Agent running in under 5 minutes:

### 1. Clone & Install
```bash
# Clone the repository
git clone https://github.com/sgk0204/Smart_Doc.git
cd smartdoc-ai-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Free API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" 
4. Copy the generated key (completely free!)

### 3. Run Application
```bash
# Start the application
streamlit run app_enhanced.py

# Or use the basic version
streamlit run app.py
```

### 4. Configure & Test
1. Open http://localhost:8501 in your browser
2. Enter your API key in the sidebar
3. Upload a PDF document
4. Start analyzing with AI!

---


## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
GEMINI_MODEL=gemini-1.5-flash
MAX_FILE_SIZE_MB=10
MAX_PAGES_FREE_TIER=5
RATE_LIMIT_DELAY=6
DEBUG=false

# Advanced Settings
SESSION_TIMEOUT=3600
CACHE_SIZE=100
LOG_LEVEL=INFO
ENABLE_ANALYTICS=false
```

### Configuration File

The `config.py` file contains all application settings:

```python
class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-1.5-flash"

    # Processing Limits
    MAX_FILE_SIZE_MB = 10
    MAX_PAGES_FREE_TIER = 5
    MAX_TEXT_LENGTH = 12000

    # Rate Limiting
    RATE_LIMIT_DELAY = 6
    REQUESTS_PER_MINUTE = 10
    DAILY_REQUEST_LIMIT = 250
```
---

## 🎮 Usage Guide

### Basic Workflow

#### 1. **Application Startup**
```bash
# Start the application
streamlit run app_enhanced.py

# Application will be available at:
# Local: http://localhost:8501
# Network: http://YOUR_IP:8501
```

#### 2. **API Configuration**
- Navigate to the sidebar
- Enter your Gemini API key
- Wait for "✅ Gemini API configured successfully!" message
- API connection is tested automatically

#### 3. **Document Upload**
- Click "Upload PDF Documents"
- Select one or more PDF files (max 10MB each)
- Files are validated automatically
- View file information: size, hash, status

#### 4. **Document Processing**
- Click "🔄 Process Documents" 
- Watch real-time progress indicators
- Review processing results and metadata
- Files are stored in session for analysis

#### 5. **AI Analysis**
- Select analysis mode from sidebar dropdown
- Choose from 5 different analysis types
- Click "🔍 Analyze" on processed documents
- View comprehensive AI-generated insights

#### 6. **Interactive Chat**
- Scroll to "💬 Interactive Document Chat"
- Ask questions about your documents
- View conversation history with timestamps
- Ask follow-up questions for deeper insights

### Advanced Features

#### Batch Processing
```python
# Process multiple documents simultaneously
1. Upload multiple PDF files
2. Click "📊 Batch Analyze"
3. Select analysis mode
4. Review comparative results
```

#### Custom Analysis
```python
# Ask specific questions
1. Select "❓ Custom Question" mode
2. Enter specific query in sidebar
3. Get targeted AI responses
4. Refine questions for better results
```

#### Session Management
```python
# Track usage and performance
- View session statistics in sidebar
- Monitor API usage and limits
- Track processed files and analyses
- Clear session data when needed
```

---

## 🔧 API Configuration

### Getting Your Gemini API Key

#### Step 1: Create Google Account
- Sign up for a free Google account if you don't have one
- No payment information required

#### Step 2: Access Google AI Studio
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Accept terms and conditions

#### Step 3: Generate API Key
1. Click "Create API Key" 
2. Select or create a project
3. Copy the generated API key
4. Store securely (never share publicly)

#### Step 4: Configure Application
```bash
# Method 1: Environment Variable
export GEMINI_API_KEY="your_api_key_here"

# Method 2: .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Method 3: Direct input in application
# Enter key in sidebar when prompted
```

### API Models Available

#### Gemini 1.5 Flash (Recommended)
- **Speed**: Fast response times
- **Free Tier**: 250 requests/day
- **Rate Limit**: 10 requests/minute
- **Best For**: General document analysis, summaries

#### Gemini 1.5 Pro
- **Quality**: Higher accuracy for complex tasks  
- **Free Tier**: 100 requests/day
- **Rate Limit**: 5 requests/minute
- **Best For**: Technical analysis, detailed insights

### Rate Limiting & Quotas

#### Free Tier Limits
```python
Daily Limits:
- Gemini 1.5 Flash: 250 requests/day
- Gemini 1.5 Pro: 100 requests/day

Rate Limits:
- Gemini 1.5 Flash: 10 requests/minute
- Gemini 1.5 Pro: 5 requests/minute

Content Limits:
- Max input tokens: 1M (Flash) / 2M (Pro)
- Max output tokens: 8K per request
```

#### Smart Rate Management
SmartDoc automatically manages rate limits:
- **Automatic pacing** between requests
- **Progress indicators** during waits
- **Error handling** for quota exceeded
- **Retry logic** for temporary failures

---

## 📊 Analysis Modes

### 1. 📝 Smart Summary
**Purpose**: Quick document overview with essential information

**Output Includes**:
- Executive summary (2-3 sentences)
- Main topics covered
- Key findings or conclusions
- Important statistics or data
- Overall assessment

**Best For**: 
- Initial document review
- Executive briefings
- Quick content understanding

**Example Use Cases**:
- Business reports
- Research paper abstracts
- Policy documents

### 2. 📊 Comprehensive Analysis
**Purpose**: Detailed document breakdown with structured insights

**Output Framework**:
1. **Document Overview** - Purpose, scope, context
2. **Key Themes & Topics** - Main subjects discussed  
3. **Critical Findings** - Important discoveries/insights
4. **Data & Evidence** - Statistics, facts, supporting info
5. **Arguments & Positions** - Main claims and reasoning
6. **Implications** - Significance and broader impact
7. **Recommendations** - Suggested actions/next steps
8. **Assessment** - Overall evaluation

**Best For**:
- Detailed document review
- Academic research
- Business analysis
- Strategic planning

### 3. 💡 Key Insights
**Purpose**: Extract and highlight the most important discoveries

**Focus Areas**:
- **Top 5 Critical Findings** - Most important discoveries
- **Trends & Patterns** - Emerging patterns in data/content
- **Implications & Impact** - Broader consequences
- **Opportunities & Challenges** - Potential and obstacles
- **Strategic Recommendations** - Actionable next steps

**Best For**:
- Decision making
- Investment analysis
- Competitive intelligence
- Trend analysis

### 4. 🔬 Technical Analysis
**Purpose**: Specialized analysis for technical and scientific documents

**Technical Framework**:
- **Methodology** - Approaches and techniques used
- **Technical Details** - Specifications and parameters
- **Data Analysis** - Statistical information interpretation
- **Technical Conclusions** - Engineering/scientific findings
- **Implementation Notes** - Practical applications

**Best For**:
- Research papers
- Technical specifications
- Engineering reports
- Scientific studies

### 5. ❓ Custom Questions
**Purpose**: Answer specific questions about document content

**Features**:
- Direct answers to user queries
- Supporting evidence from document
- Context and background explanation
- Implications and significance
- Limitations and caveats noted

**Best For**:
- Targeted information extraction
- Specific fact-finding
- Compliance checking
- Detail clarification

### Analysis Comparison Table

| Mode | Time | Detail Level | Best Use Case | Output Length |
|------|------|--------------|---------------|---------------|
| Smart Summary | ~30s | Low | Quick overview | 200 words |
| Comprehensive | ~60s | High | Detailed review | 800 words |
| Key Insights | ~45s | Medium | Decision making | 500 words |
| Technical | ~50s | High | Scientific docs | 700 words |
| Custom Q&A | ~40s | Variable | Specific queries | 400 words |

---

## 💬 Interactive Features

### Document Chat Interface

#### Starting a Conversation
```python
1. Process documents first
2. Navigate to "💬 Interactive Document Chat"
3. Type your question in the input field
4. Click "🔍 Ask Question"
5. View AI response with citations
```

#### Sample Questions
```python
General Questions:
- "What are the main conclusions in this document?"
- "What are the key findings and recommendations?"
- "Are there any risks or challenges mentioned?"

Technical Questions:
- "What technical requirements are specified?"
- "What methodologies were used in this research?"
- "What are the implementation steps outlined?"

Business Questions:
- "What are the financial implications discussed?"
- "What market opportunities are identified?"
- "What competitive advantages are mentioned?"
```

#### Chat Features

##### Conversation History
- All interactions are saved with timestamps
- Navigate through previous questions and answers
- Clear chat history when needed
- Export conversations for reference

##### Multi-Turn Dialogue
```python
Follow-up Questions:
User: "What are the main benefits?"
AI: [Provides detailed benefits analysis]

User: "Can you elaborate on the cost savings?"
AI: [Focuses specifically on cost-related benefits]

User: "What are the implementation challenges?"
AI: [Discusses potential obstacles and solutions]
```

##### Context Awareness
- AI remembers previous questions in conversation
- Maintains context across multiple exchanges
- References earlier parts of discussion
- Builds on previous insights

#### Advanced Chat Commands

##### Document Summary
```python
# Generate multi-document summary
Click "📋 Document Summary" button
- Combines insights from all processed documents
- Identifies common themes across files
- Highlights contradictions or differences
- Provides consolidated recommendations
```

##### Conversation Export
```python
# Save chat history
conversations = {
    "session_id": "unique_session_id",
    "timestamp": "2025-09-20T11:45:00",
    "messages": [
        {"role": "user", "content": "What are the key points?"},
        {"role": "assistant", "content": "The key points include..."}
    ]
}
```

---


## 📁 File Descriptions

### Core Application Files

#### `app.py` - Basic Application
```python
"""
Basic SmartDoc AI Agent with core functionality
- Simple document upload and processing  
- Basic AI analysis capabilities
- Minimal UI with essential features
- Perfect for learning and testing
"""
Features:
- Single document processing
- 3 analysis modes
- Basic error handling
- ~500 lines of code
```

#### `app_enhanced.py` - Full-Featured Application  
```python
"""
Enhanced version with advanced capabilities
- Multi-document support
- Interactive chat interface
- Session management
- Comprehensive analytics
"""
Features:
- Batch processing
- 5 analysis modes
- Chat interface
- Session statistics
- Advanced error handling
- ~1000+ lines of code
```

### Configuration Files

#### `config.py` - Main Configuration
```python
"""
Central configuration management
"""
class Config:
    # API settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-1.5-flash"

    # Processing limits
    MAX_FILE_SIZE_MB = 10
    MAX_PAGES_FREE_TIER = 5

    # Rate limiting
    RATE_LIMIT_DELAY = 6
    REQUESTS_PER_MINUTE = 10
```


### Utility Files

#### `utils.py` - Helper Functions
```python
"""
Common utility functions
"""
Functions:
- validate_pdf_file() - File validation
- format_file_size() - Size formatting
- clean_text() - Text processing
- extract_pdf_metadata() - Metadata extraction
- SessionStateManager - State management
```

### Documentation Files

#### `requirements.txt` - Dependencies
```txt
streamlit>=1.28.0
google-generativeai>=0.3.2
PyPDF2>=3.0.1
python-dotenv>=1.0.0
numpy>=1.24.3
typing-extensions>=4.8.0
```
---
