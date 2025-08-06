from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional

from pydantic import BaseModel, Field


class AIMessage(BaseModel):
    """Standardized AI message format"""

    role: str = Field(description="Role of the message sender")
    content: str = Field(description="Message Content")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional Metadata"
    )


class AIResponse(BaseModel):
    """Standardized AI response format"""

    content: str = Field(description="Response content")
    usage: Optional[Dict[str, Any]] = Field(
        default=None, description="Token usage information"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: str, model_name: str, **kwargs: Any):
        super().__init__()
        self.api_key = api_key
        self.model_name = model_name
        self.config = kwargs

    @abstractmethod
    async def generate_response(
        self, messages: List[AIMessage], **kwargs: Any
    ) -> AIResponse:
        """Generate a response from the AI model."""
        pass

    @abstractmethod
    async def stream_response(
        self, messages: List[AIMessage], **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the AI model."""
        # This construct satisfies type checkers that this is an async generator
        # without adding any runtime overhead, resolving the override error.
        if False:
            yield

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider configuration."""
        pass
