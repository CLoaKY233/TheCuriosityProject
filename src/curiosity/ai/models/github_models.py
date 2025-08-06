from typing import Any, AsyncGenerator, Dict, List

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from ..exceptions import AIAPIError, AIConfigurationError
from ..interface import AIMessage, AIProvider, AIResponse


class GithubModelsProvider(AIProvider):
    """Github Models AI provider implementation"""

    def __init__(
        self,
        api_key: str,
        model_name: str = "openai/gpt-4o",
        endpoint: str = "https://models.github.ai/inference",
        **kwargs: Any,
    ):
        super().__init__(api_key, model_name, **kwargs)
        self.endpoint = endpoint
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Github Models client"""
        try:
            self.client = ChatCompletionsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.api_key),
            )
        except Exception as e:
            raise AIConfigurationError(
                f"Failed to initialize GitHub Models client: {str(e)}",
                provider="github",
            )

    async def generate_response(
        self, messages: List[AIMessage], **kwargs: Any
    ) -> AIResponse:
        """Generate a response using GitHub Models."""
        if not self.client:
            raise AIConfigurationError(
                "GitHub Models client not initialized",
                provider="github",
            )

        try:
            # Convert AIMessage to Dict format for Azure API
            formatted_messages: List[Dict[str, Any]] = []
            for msg in messages:
                formatted_messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "metadata": msg.metadata,
                    }
                )

            response = self.client.complete(
                messages=formatted_messages,
                model=self.model_name,
                temperature=kwargs.get("temperature", 1.0),
                top_p=kwargs.get("top_p", 1.0),
            )

            return AIResponse(
                content=response.choices[0].message.content,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens
                    if response.usage
                    else None,
                    "completion_tokens": response.usage.completion_tokens
                    if response.usage
                    else None,
                    "total_tokens": response.usage.total_tokens
                    if response.usage
                    else None,
                },
                metadata={
                    "model": self.model_name,
                    "provider": "github",
                },
            )
        except Exception as e:
            raise AIAPIError(f"GitHub Models API error: {str(e)}", provider="github")

    async def stream_response(
        self, messages: List[AIMessage], **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream response from GitHub Models."""
        if not self.client:
            raise AIConfigurationError(
                "GitHub Models client not initialized",
                provider="github",
            )

        try:
            formatted_messages: List[Dict[str, Any]] = []
            for msg in messages:
                formatted_messages.append(
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "metadata": msg.metadata,
                    }
                )

            response = self.client.complete(
                stream=True,
                messages=formatted_messages,
                model=self.model_name,
                temperature=kwargs.get("temperature", 1.0),
                top_p=kwargs.get("top_p", 1.0),
            )

            for update in response:
                if update.choices and update.choices[0].delta:
                    content = update.choices[0].delta.content
                    if content:
                        yield content
        except Exception as e:
            raise AIAPIError(
                f"GitHub Models streaming error: {str(e)}",
                provider="github",
            )

    def validate_config(self) -> bool:
        """Validate GitHub Models configuration."""
        return bool(self.api_key and self.model_name and self.endpoint and self.client)
