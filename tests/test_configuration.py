import pytest
from pydantic import ValidationError

from template_rooms_pkg.configuration.addonconfig import CustomAddonConfig
from template_rooms_pkg.configuration.baseconfig import BaseAddonConfig


class TestBaseAddonConfig:
    def test_base_config_creation(self):
        config = BaseAddonConfig(
            id="test_addon_id",
            type="test_type",
            name="test_addon",
            description="Test addon description",
            secrets={"key1": "value1"}
        )

        assert config.id == "test_addon_id"
        assert config.type == "test_type"
        assert config.name == "test_addon"
        assert config.description == "Test addon description"
        assert config.secrets == {"key1": "value1"}
        assert config.enabled is True

    def test_base_config_defaults(self):
        config = BaseAddonConfig(
            id="test_id",
            type="test_type",
            name="test",
            description="Test description"
        )

        assert config.enabled is True
        assert config.secrets == {}
        assert config.config == {}


class TestCustomAddonConfig:
    def test_custom_config_creation_success(self):
        config = CustomAddonConfig(
            id="test_addon_id",
            type="example",
            name="test_addon",
            description="Test addon",
            example_param1="value1",
            example_param2="custom_value",
            example_param3=9999,
            secrets={"example_api_key": "key123", "example_secret": "secret456"}
        )

        assert config.id == "test_addon_id"
        assert config.name == "test_addon"
        assert config.type == "example"
        assert config.example_param1 == "value1"
        assert config.example_param2 == "custom_value"
        assert config.example_param3 == 9999

    def test_custom_config_with_defaults(self):
        config = CustomAddonConfig(
            id="test_addon_id",
            type="example",
            name="test_addon",
            description="Test addon",
            example_param1="value1",
            secrets={"example_api_key": "key123", "example_secret": "secret456"}
        )

        assert config.example_param2 == "default_value"
        assert config.example_param3 == 5432

    def test_custom_config_missing_api_key(self):
        with pytest.raises(ValidationError, match="Missing required secrets"):
            CustomAddonConfig(
                id="test_addon_id",
                type="example",
                name="test_addon",
                description="Test addon",
                example_param1="value1",
                secrets={"example_secret": "secret456"}
            )

    def test_custom_config_missing_secret(self):
        with pytest.raises(ValidationError, match="Missing required secrets"):
            CustomAddonConfig(
                id="test_addon_id",
                type="example",
                name="test_addon",
                description="Test addon",
                example_param1="value1",
                secrets={"example_api_key": "key123"}
            )

    def test_custom_config_missing_both_secrets(self):
        with pytest.raises(ValidationError, match="Missing required secrets"):
            CustomAddonConfig(
                id="test_addon_id",
                type="example",
                name="test_addon",
                description="Test addon",
                example_param1="value1",
                secrets={}
            )

    def test_custom_config_missing_required_fields(self):
        with pytest.raises(ValidationError):
            CustomAddonConfig(
                id="test_addon_id",
                type="example",
                name="test_addon",
                description="Test addon",
                secrets={"example_api_key": "key123", "example_secret": "secret456"}
            )
