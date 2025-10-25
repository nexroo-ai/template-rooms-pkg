from pydantic import Field, model_validator

from ..baseconfig import BaseAddonConfig, RequiredSecretsBase


class CustomRequiredSecrets(RequiredSecretsBase):
    api_key: str = Field(..., description="API key environment variable name")


class CustomAddonConfig(BaseAddonConfig):
    """API addon example"""

    endpoint: str = Field(..., description="API endpoint URL")
    method: str = Field("GET", description="HTTP method")
    timeout: int = Field(30, description="Request timeout")

    @classmethod
    def get_required_secrets(cls) -> CustomRequiredSecrets:
        return CustomRequiredSecrets(api_key="api_key")

    @model_validator(mode='after')
    def validate_api_config(self):
        required_secrets_config = self.get_required_secrets()
        required_secrets = list(required_secrets_config.model_fields.keys())
        missing = [s for s in required_secrets if s not in self.secrets]
        if missing:
            raise ValueError(f"Missing API secrets: {missing}")

        if not self.endpoint.startswith(('http://', 'https://')):
            raise ValueError("endpoint must be a valid URL")

        return self
