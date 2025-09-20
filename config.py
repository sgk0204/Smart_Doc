"""
Configuration settings for SmartDoc AI Agent (REVISED VERSION)
All API configurations updated for proper Gemini API usage
"""
import os
from typing import Dict, Any, List

class Config:
    """Application configuration class - REVISED for correct Gemini API"""

    # API Configuration - UPDATED FOR CORRECT GEMINI API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Available models with their specifications
    AVAILABLE_MODELS = {
        'gemini-1.5-flash': {
            'name': 'Gemini 1.5 Flash',
            'description': 'Fast and efficient for most document analysis tasks',
            'free_tier': True,
            'rate_limit_rpm': 10,  # requests per minute
            'rate_limit_rpd': 250, # requests per day
            'context_window': 1000000,  # 1M tokens
            'recommended_use': 'General document analysis, summaries, Q&A'
        },
        'gemini-1.5-pro': {
            'name': 'Gemini 1.5 Pro', 
            'description': 'Advanced model for complex analysis and reasoning',
            'free_tier': True,
            'rate_limit_rpm': 5,   # requests per minute
            'rate_limit_rpd': 100, # requests per day
            'context_window': 2000000,  # 2M tokens
            'recommended_use': 'Complex analysis, technical documents, detailed insights'
        }
    }

    # Default model selection
    DEFAULT_MODEL = 'gemini-1.5-flash'  # Fast and reliable for most use cases
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    # Document Processing Configuration
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_FORMATS = ['.pdf']
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # Free Tier Optimizations
    FREE_TIER_LIMITS = {
        'max_pages_per_document': 5,
        'max_text_length': 12000,  # characters per analysis
        'max_concurrent_requests': 1,
        'rate_limit_delay': 6,     # seconds between requests
        'daily_request_limit': 250,
        'monthly_request_limit': 7500
    }

    # Analysis Modes Configuration
    ANALYSIS_MODES = {
        'summary': {
            'name': 'Smart Summary',
            'description': 'Concise overview with key points',
            'icon': '📝',
            'max_length': 300,
            'focus': 'brevity'
        },
        'comprehensive': {
            'name': 'Comprehensive Analysis',
            'description': 'Detailed breakdown with all sections',
            'icon': '📊',
            'max_length': 1000,
            'focus': 'depth'
        },
        'insights': {
            'name': 'Key Insights',
            'description': 'Important findings and patterns',
            'icon': '💡',
            'max_length': 500,
            'focus': 'insights'
        },
        'technical': {
            'name': 'Technical Analysis',
            'description': 'Technical details and methodology',
            'icon': '🔬',
            'max_length': 800,
            'focus': 'technical'
        },
        'custom': {
            'name': 'Custom Question',
            'description': 'Answer specific questions',
            'icon': '❓',
            'max_length': 600,
            'focus': 'targeted'
        }
    }

    # Streamlit Configuration
    PAGE_CONFIG = {
        'page_title': "SmartDoc AI Agent",
        'page_icon': "📚",
        'layout': "wide",
        'initial_sidebar_state': "expanded"
    }

    # UI Text and Messages
    MESSAGES = {
        'success': {
            'api_configured': "✅ Gemini API configured successfully!",
            'document_processed': "✅ Document processed successfully!",
            'analysis_complete': "✅ Analysis completed successfully!",
            'files_uploaded': "✅ Files uploaded and validated successfully!",
            'text_extracted': "✅ Text extracted from {} pages",
            'batch_complete': "🎉 Batch analysis completed for {} documents!"
        },
        'error': {
            'no_api_key': "❌ Please set your GEMINI_API_KEY",
            'invalid_api_key': "🔑 Invalid API key. Please check your Gemini API key.",
            'api_quota_exceeded': "🚫 API quota exceeded. Try again later or upgrade.",
            'file_too_large': f"📄 File too large. Maximum size: {MAX_FILE_SIZE_MB}MB",
            'unsupported_format': f"📄 Unsupported format. Supported: {', '.join(SUPPORTED_FORMATS)}",
            'processing_error': "❌ Error processing document. Please try again.",
            'analysis_error': "❌ Analysis failed. Please check your query and try again.",
            'connection_error': "🌐 Connection failed. Check internet connection.",
            'permission_denied': "🚫 Permission denied. Check API key permissions.",
            'resource_exhausted': "🚫 Resources exhausted. Too many requests.",
            'no_text_content': "📄 No readable text found in document.",
            'file_corrupted': "📄 File appears to be corrupted or empty."
        },
        'warning': {
            'quota_warning': "⚠️ Approaching daily quota limit",
            'large_file': "⚠️ Large file may take longer to process",
            'content_truncated': "⚠️ Content truncated for free tier optimization",
            'multiple_pages': "⚠️ PDF has {} pages, analyzing first {} (free tier limit)",
            'api_key_short': "⚠️ API key appears too short",
            'slow_response': "⏳ Analysis taking longer than expected..."
        },
        'info': {
            'get_api_key': "💡 Get your free API key from: https://aistudio.google.com/app/apikey",
            'free_tier': "🆓 Using free tier - 250 requests/day available",
            'processing_tips': "💡 For better results, use clear, high-quality PDFs",
            'rate_limiting': "⏳ Rate limiting active to respect free tier limits",
            'batch_processing': "📊 Processing multiple documents in batch mode"
        }
    }

    # Error Handling Configuration
    ERROR_RETRY_CONFIG = {
        'max_retries': 3,
        'retry_delay': 2,  # seconds
        'exponential_backoff': True,
        'retry_on_errors': [
            'RESOURCE_EXHAUSTED',
            'DEADLINE_EXCEEDED',
            'UNAVAILABLE'
        ]
    }

    # Logging Configuration
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'log_api_calls': True,
        'log_file_processing': True,
        'log_user_interactions': False  # Privacy setting
    }

    @classmethod
    def get_model_config(cls, model_name: str = None) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        model_name = model_name or cls.GEMINI_MODEL
        return cls.AVAILABLE_MODELS.get(model_name, cls.AVAILABLE_MODELS[cls.DEFAULT_MODEL])

    @classmethod
    def is_free_tier_model(cls, model_name: str = None) -> bool:
        """Check if model is available in free tier"""
        model_config = cls.get_model_config(model_name)
        return model_config.get('free_tier', False)

    @classmethod
    def get_rate_limits(cls, model_name: str = None) -> Dict[str, int]:
        """Get rate limits for a model"""
        model_config = cls.get_model_config(model_name)
        return {
            'requests_per_minute': model_config.get('rate_limit_rpm', 10),
            'requests_per_day': model_config.get('rate_limit_rpd', 250)
        }

    @classmethod
    def validate_config(cls) -> Tuple[bool, List[str]]:
        """Validate configuration settings"""
        errors = []

        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY not set")

        if cls.GEMINI_MODEL not in cls.AVAILABLE_MODELS:
            errors.append(f"Invalid model: {cls.GEMINI_MODEL}")

        if cls.MAX_FILE_SIZE_MB <= 0:
            errors.append("Invalid max file size")

        return len(errors) == 0, errors

    @classmethod
    def get_analysis_mode_config(cls, mode: str) -> Dict[str, Any]:
        """Get configuration for analysis mode"""
        return cls.ANALYSIS_MODES.get(mode, cls.ANALYSIS_MODES['summary'])

# Environment-specific configurations
DEVELOPMENT_CONFIG = {
    'debug': True,
    'detailed_errors': True,
    'log_level': 'DEBUG',
    'cache_responses': False,
    'show_performance_metrics': True
}

PRODUCTION_CONFIG = {
    'debug': False,
    'detailed_errors': False,
    'log_level': 'WARNING',
    'cache_responses': True,
    'show_performance_metrics': False
}

# Free tier specific optimizations
FREE_TIER_OPTIMIZATIONS = {
    'enable_caching': True,
    'compress_text': True,
    'batch_requests': True,
    'smart_chunking': True,
    'rate_limit_buffer': 1.2,  # 20% safety margin
    'priority_queue': True
}

# Security settings
SECURITY_CONFIG = {
    'sanitize_input': True,
    'validate_file_headers': True,
    'max_upload_size_bytes': Config.MAX_FILE_SIZE_MB * 1024 * 1024,
    'allowed_file_extensions': Config.SUPPORTED_FORMATS,
    'api_key_validation': True,
    'rate_limit_enforcement': True
}
