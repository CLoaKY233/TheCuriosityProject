from typing import Any, Dict, Optional


class AIProviderError(Exception):
    """Base exception for AI provided errors"""

    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.provider = provider
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class AIConfigurationError(AIProviderError):
    """Raised whenn AI Provider configuration is invalid"""

    pass


class AIAPIError(AIProviderError):
    """Raised when AI API calls fail"""

    pass


class AIModelNotFoundError(AIProviderError):
    """Raised when spevified AI model is not found"""

    pass
