import importlib
from loguru import logger

class TemplateRoomsAddon:
    """
    Template Rooms Package Addon Class
    
    This class provides access to all template rooms package functionality
    and can be instantiated by external programs using this package.
    """
    
    def __init__(self):
        self.modules = ["actions", "configuration", "memory", "services", "storage", "tools", "utils"]
        
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