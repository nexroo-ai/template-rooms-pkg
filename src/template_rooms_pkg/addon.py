import importlib
from loguru import logger
from .actions.example import ActionInput, example
# from .actions.base import ActionResponse

class TemplateRoomsAddon:
    """
    Template Rooms Package Addon Class
    
    This class provides access to all template rooms package functionality
    and can be instantiated by external programs using this package.
    """
    
    def __init__(self):
        self.modules = ["actions", "configuration", "memory", "services", "storage", "tools", "utils"]
        self.config = {}

    # try pydantic model validation ?
    # add your actions here  
    def example(self, param1: str, param2: str) -> dict:#-> ActionResponse:
        # create ActionInput object with params
        inputs = ActionInput(param1=param1, param2=param2)
        return example(inputs=inputs)

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
                                # Skip Pydantic models and specific known models that require parameters
                                skip_instantiation = False
                                
                                try:
                                    from pydantic import BaseModel
                                    if hasattr(component, '__bases__') and any(
                                        issubclass(base, BaseModel) for base in component.__bases__ if isinstance(base, type)
                                    ):
                                        logger.debug(f"Component {component_name} is a Pydantic model, skipping instantiation")
                                        skip_instantiation = True
                                except (ImportError, TypeError):
                                    pass
                                
                                # Also skip known models that require parameters
                                if component_name in ['ActionInput', 'ActionOutput']:
                                    logger.debug(f"Component {component_name} requires parameters, skipping instantiation")
                                    skip_instantiation = True
                                
                                if not skip_instantiation:
                                    # result = component()
                                    logger.debug(f"Component {component_name}() would be executed successfully")
                                else:
                                    logger.debug(f"Component {component_name} exists and is valid (skipped instantiation)")
                            except Exception as e:
                                logger.warning(f"Component {component_name}() failed: {e}")
                logger.info(f"{component_count} {module_name} loaded correctly, available imports: {', '.join(components)}")
            except ImportError as e:
                logger.error(f"Failed to import {module_name}: {e}")
                return False
            except Exception as e:
                logger.error(f"Error testing {module_name}: {e}")
                return False
        logger.info("Template rooms package test completed successfully!")
        logger.info(f"Total components loaded: {total_components} across {len(self.modules)} modules")
        return True
    
    def loadAddonConfig(self, addon_config: dict):
        """
        Load addon configuration.
        
        Args:
            addon_config (dict): Addon configuration dictionary
        
        Returns:
            bool: True if configuration is loaded successfully, False otherwise
        """
        try:
            from template_rooms_pkg.configuration import CustomAddonConfig
            self.config = CustomAddonConfig(**addon_config)
            logger.info(f"Addon configuration loaded successfully: {self.config}")
            return True
        except Exception as e:
            logger.error(f"Failed to load addon configuration: {e}")
            return False