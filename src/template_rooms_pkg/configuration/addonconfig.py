from pydantic import Field, model_validator

from .baseconfig import BaseAddonConfig, RequiredSecretsBase


class CustomRequiredSecrets(RequiredSecretsBase):
    example_api_key: str = Field(..., description="Example API key environment variable name")
    example_secret: str = Field(..., description="Example secret environment variable name")


class CustomAddonConfig(BaseAddonConfig):
    example_param1: str = Field(..., description="Example required parameter")
    example_param2: str = Field("default_value", description="Example optional parameter with default")
    example_param3: int = Field(5432, description="Example integer parameter")

    @classmethod
    def get_required_secrets(cls) -> CustomRequiredSecrets:
        return CustomRequiredSecrets(
            example_api_key="example_api_key",
            example_secret="example_secret"
        )

    @model_validator(mode='after')
    def validate_addon_secrets(self):
        required_secrets_config = self.get_required_secrets()
        required_secrets = list(required_secrets_config.model_fields.keys())
        missing = [s for s in required_secrets if s not in self.secrets]
        if missing:
            raise ValueError(f"Missing required secrets: {missing}")
        return self
