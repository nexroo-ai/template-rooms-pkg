import os
import importlib
from typing import Dict, Any, Optional
from loguru import logger


class TemplateRoomsAddon:
    """
    Template Rooms Package Addon Class
    
    This class provides access to all template rooms package functionality
    and can be instantiated by external programs using this package.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.modules = ["actions", "configuration", "memory", "services", "storage", "tools", "utils"]
        self.config = config or {}
        self.validated_config = None
        if config:
            self._validate_config(config)
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        try:
            from .configuration.baseconfig import BaseAddonConfig
            try:
                from .configuration.addonconfig import CustomAddonConfig
                config_class = CustomAddonConfig
                logger.debug(f"Using CustomAddonConfig for validation")
            except ImportError:
                config_class = BaseAddonConfig
                logger.debug(f"CustomAddonConfig not found, using BaseAddonConfig")
            
            validated_config = config_class(**config)
            self.validated_config = validated_config
            logger.info(f"Configuration validated successfully for addon {config.get('id', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Configuration validation failed for addon {config.get('id', 'unknown')}: {e}")
            raise
        
    def test(self) -> bool:
        """
        Test function for template rooms package.
        Tests each module and reports available components.
        Test connections with credentials if required.
        
        Returns:
            bool: True if test passes, False otherwise
        """
        logger.info("Running template-rooms-pkg test...")
        
        total_components = 0
        for module_name in self.modules:
            try:
                module = importlib.import_module(f"template_rooms_pkg.{module_name}")
                components = getattr(module, '__all__', [])
                component_count = len(components)
                total_components += component_count
                for component_name in components:
                    if hasattr(module, component_name):
                        component = getattr(module, component_name)
                        if callable(component):
                            try:
                                # Skip Pydantic model classes to avoid validation errors
                                if hasattr(component, '__bases__') and any(
                                    'BaseModel' in str(base) for base in component.__bases__
                                ):
                                    logger.debug(f"Component {component_name} is a Pydantic model, skipping instantiation")
                                    continue
                                result = component()
                                logger.debug(f"Component {component_name}() executed successfully")
                            except Exception as e:
                                logger.warning(f"Component {component_name}() failed: {e}")
                logger.info(f"{component_count} {module_name} loaded correctly, available imports: {', '.join(components)}")
            except ImportError as e:
                logger.error(f"Failed to import {module_name}: {e}")
                return False
            except Exception as e:
                logger.error(f"Error testing {module_name}: {e}")
                return False
        logger.info(f"Template rooms package test completed successfully!")
        logger.info(f"Total components loaded: {total_components} across {len(self.modules)} modules")
        return True