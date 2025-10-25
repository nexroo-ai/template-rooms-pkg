from pydantic import Field, model_validator

from ..baseconfig import BaseAddonConfig, RequiredSecretsBase


class CustomRequiredSecrets(RequiredSecretsBase):
    db_password: str = Field(..., description="Database password environment variable name")
    db_user: str = Field(..., description="Database user environment variable name")


class CustomAddonConfig(BaseAddonConfig):
    """Database addon example"""

    host: str = Field(..., description="Database host")
    database: str = Field(..., description="Database name")
    port: int = Field(5432, description="Database port")

    @classmethod
    def get_required_secrets(cls) -> CustomRequiredSecrets:
        return CustomRequiredSecrets(
            db_password="db_password",
            db_user="db_user"
        )

    @model_validator(mode='after')
    def validate_db_secrets(self):
        required_secrets_config = self.get_required_secrets()
        required_secrets = list(required_secrets_config.model_fields.keys())
        missing = [s for s in required_secrets if s not in self.secrets]
        if missing:
            raise ValueError(f"Missing database secrets: {missing}")
        return self
