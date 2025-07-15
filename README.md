# Template Rooms Package

A template Python package for the AI rooms script addon system.

## Overview

This package provides a basic template implementation for creating addon packages that can be loaded by the AI rooms script. It includes an addon class with a `test()` method that validates the package functionality.

## Installation

```bash
pip install -e .
```

## Usage

This package is designed to be imported by the AI rooms script's `loadAddons` functionality. The package provides an addon class that can be instantiated and used:

```python
from template_rooms_pkg.addon import TemplateRoomsAddon

# Instantiate the addon
addon = TemplateRoomsAddon()

# Test the addon functionality
result = addon.test()
```

The AI rooms script automatically discovers and instantiates the addon class from the `addon.py` module, so manual instantiation is typically not required in production use.

## Creating a New Addon from Template

To create a new addon package using this template:

1. **Clone or fork this repository**
2. **Rename the package directory and references:**
   - Rename `src/template_rooms_pkg/` to `src/{your_addon_name}_rooms_pkg/`
   - Update `pyproject.toml`:
     - Change package name from `template-rooms-pkg` to `{your-addon-name}-rooms-pkg`
     - Update module path in `[tool.setuptools.packages.find]`
   - Update imports in `src/{your_addon_name}_rooms_pkg/addon.py`
3. **Update the addon class:**
   - Rename `TemplateRoomsAddon` to `{YourAddonName}RoomsAddon` in `addon.py`
   - Customize the `test()` method and add your addon functionality
4. **Create configuration schema:**
   - Define your addon's configuration schema in `configuration/` directory
   - Inherit from `BaseAddonConfig` for validation
5. **Update documentation:**
   - Modify this README.md with your addon's specific information
   - Update the CHANGELOG.md

### Required File Structure
```
src/
└── {your_addon_name}_rooms_pkg/
    ├── __init__.py
    ├── addon.py              # Contains your addon class
    ├── actions/
    ├── configuration/
    ├── memory/
    ├── services/
    ├── storage/
    ├── tools/
    └── utils/
```

## CI/CD

The project uses semantic release for automated versioning and publishing:

- **Automated Versioning**: Semantic release analyzes commit messages to determine version bumps
- **Automated Publishing**: Releases are triggered automatically on pushes to the main branch
- **Commit Message Format**: Follow conventional commits format:
  - `feat:` for new features (minor version)
  - `fix:` for bug fixes (patch version)  
  - `BREAKING CHANGE:` for breaking changes (major version)

### Release Process
1. Push changes to main branch
2. Semantic release automatically:
   - Analyzes commit history
   - Determines next version number
   - Generates changelog
   - Creates GitHub release
   - Publishes to PyPI (if configured)

## Addon Configuration

### Setup Configuration Schema

1. **Create your config class** in `configuration/addonconfig.py`:

```python
from pydantic import Field, model_validator
from template_rooms_pkg.configuration.baseconfig import BaseAddonConfig

class CustomAddonConfig(BaseAddonConfig):
    type: str = Field("your_addon_type", description="Your addon type")
    
    # Add required fields
    required_field: str = Field(..., description="Required field")
    
    # Add optional fields with defaults
    optional_field: int = Field(30, description="Optional field")
    
    @model_validator(mode='after')
    def validate_configuration(self):
        # Validate required secrets
        if "required_secret" not in self.secrets:
            raise ValueError("required_secret is missing")
        
        # Add custom validation
        if self.optional_field < 0:
            raise ValueError("optional_field must be positive")
            
        return self
```

2. **Update** `configuration/__init__.py`:

```python
from .baseconfig import BaseAddonConfig
from .your_addon_config import CustomAddonConfig

__all__ = ["BaseAddonConfig", "CustomAddonConfig"]
```

### Examples

See `configuration/examples/` for reference implementations:
- `llm_config.py` - LLM addon configuration
- `database_config.py` - Database addon configuration  
- `api_config.py` - API addon configuration

### JSON Configuration

The main script will validate this JSON against your schema:

```json
{
    "id": "your-addon-1",
    "type": "your_addon_type",
    "name": "Your Addon",
    "description": "Your addon description",
    "enabled": true,
    "required_field": "value",
    "optional_field": 60,
    "config": {
        "extra_setting": "value"
    },
    "secrets": {
        "required_secret": "ENV_VAR_NAME"
    }
}
```


## Development

The project uses semantic release for automated versioning. Releases are triggered automatically on pushes to the main branch.

## License

MIT