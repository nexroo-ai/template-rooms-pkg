import importlib
from loguru import logger
from .actions.example import example
# from .actions.base import ActionResponse
from .actions.example import ActionInput as ExampleActionInput
import inspect
from pydantic import BaseModel

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
    def example(self, input: ExampleActionInput) -> dict:#-> ActionResponse:
        return example(input)
            
    def test(self) -> bool:
        logger.info("Running template-rooms-pkg test...")
        total_components = 0

        for module_name in self.modules:
            try:
                module = importlib.import_module(f"template_rooms_pkg.{module_name}")
                components = getattr(module, '__all__', [])
                component_count = len(components)
                total_components += component_count

                for component_name in components:
                    if not hasattr(module, component_name):
                        continue

                    component = getattr(module, component_name)

                    if callable(component):
                        try:
                            sig = inspect.signature(component)
                            # Skip functions/classes that require pydantic or any non-default params
                            if any(
                                param.default is inspect.Parameter.empty and
                                param.annotation != inspect.Parameter.empty and
                                isinstance(param.annotation, type) and
                                issubclass(param.annotation, BaseModel)
                                for param in sig.parameters.values()
                            ):
                                logger.debug(f"Skipping {component_name}: requires pydantic input")
                                continue

                            if len(sig.parameters) == 0:
                                # Safe to execute
                                try:
                                    result = component()
                                    logger.debug(f"{component_name}() executed successfully with result: {result}")
                                except Exception as e:
                                    logger.warning(f"Execution of {component_name}() failed: {e}")
                            else:
                                logger.debug(f"Component {component_name} requires parameters, not calling")

                        except Exception as e:
                            logger.warning(f"Error inspecting or calling {component_name}: {e}")
                    else:
                        logger.debug(f"{component_name} is not callable")

                logger.info(f"{component_count} from '{module_name}' loaded: {', '.join(components)}")

            except ImportError as e:
                logger.error(f"Failed to import module '{module_name}': {e}")
                return False
            except Exception as e:
                logger.error(f"Error processing module '{module_name}': {e}")
                return False

        logger.info("Template rooms package test completed successfully!")
        logger.info(f"Total components loaded: {total_components} across {len(self.modules)} modules")
        return True

        
    def test_old(self) -> bool:
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
                                try:
                                    from pydantic import BaseModel
                                    if hasattr(component, '__bases__') and any(
                                        issubclass(base, BaseModel) for base in component.__bases__ if isinstance(base, type)
                                    ):
                                        logger.debug(f"Component {component_name} is a Pydantic model, skipping instantiation")
                                        continue
                                except (ImportError, TypeError):
                                    pass
                                
                                # result = component()
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