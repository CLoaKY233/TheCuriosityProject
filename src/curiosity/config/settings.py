from typing import Literal, Optional

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration settings"""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    url: str = Field(
        default="wss://cloakystores-06a9f7u3jlrsf43q77o8ttu1kk.aws-euw1.surreal.cloud",
        description="SurrealDB connection URL",
    )
    username: str = Field(default="cloaky", description="Database username")
    password: Optional[SecretStr] = Field(
        default=None, description="Database password"
    )
    namespace: str = Field(
        default="curiosity", description="Database namespace"
    )
    database: str = Field(default="curiosity", description="Database name")

    @model_validator(mode="after")
    def validate_password(self):
        if self.password is None:
            raise ValueError("Database password must be provided")
        return self


class AISettings(BaseSettings):
    """AI model configuration settings"""

    model_config = SettingsConfigDict(
        env_prefix="AI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    provider: Literal["gemini", "github", "openai"] = Field(
        default="gemini", description="AI model provider"
    )
    model_name: str = Field(
        default="gemini-1.5-flash", description="Specific model name"
    )
    api_key: Optional[SecretStr] = Field(
        default=None, description="API key for the AI service"
    )
    github_endpoint: str = Field(
        default="https://models.github.ai/inference",
        description="GitHub Models endpoint",
    )
    azure_endpoint: Optional[str] = Field(
        default=None, description="Azure AI endpoint"
    )

    @model_validator(mode="after")
    def validate_api_key(self):
        if self.api_key is None:
            raise ValueError("AI API key must be provided")
        return self


class AppSettings(BaseSettings):
    """Main Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    app_name: str = Field(default="Curiosity", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )
    database: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings()
    )
    ai: AISettings = Field(default_factory=lambda: AISettings())


settings = AppSettings()
