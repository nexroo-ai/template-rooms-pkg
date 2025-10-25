from pydantic import Field, model_validator

from ..baseconfig import BaseAddonConfig, RequiredSecretsBase


class CustomRequiredSecrets(RequiredSecretsBase):
    api_key: str = Field(..., description="LLM API key environment variable name")


class CustomAddonConfig(BaseAddonConfig):
    """LLM addon - just inherit and add what you need"""

    provider: str = Field(..., description="LLM provider (openai, anthropic, etc)")
    model: str = Field(..., description="Model name")
    temperature: float = Field(0.7, description="Temperature setting")
    max_tokens: int = Field(1000, description="Max tokens")

    @classmethod
    def get_required_secrets(cls) -> CustomRequiredSecrets:
        return CustomRequiredSecrets(api_key="api_key")

    @model_validator(mode='after')
    def validate_llm_secrets(self):
        required_secrets_config = self.get_required_secrets()
        required_secrets = list(required_secrets_config.model_fields.keys())
        missing = [s for s in required_secrets if s not in self.secrets]
        if missing:
            raise ValueError(f"Missing LLM secrets: {missing}")
        return self
