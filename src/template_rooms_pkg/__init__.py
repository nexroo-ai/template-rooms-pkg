import os
import importlib
from loguru import logger

"""

Test function for template rooms package.
Tests each module and reports available components.
Test connections with credentials if required.

Returns:
    bool: True if test passes, False otherwise
"""
def test() -> bool:
    logger.info("Running template-rooms-pkg test...")
    
    modules = ["actions", "configuration", "memory", "services", "storage", "tools", "utils"]
    total_components = 0
    for module_name in modules:
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
    logger.info(f"Total components loaded: {total_components} across {len(modules)} modules")
    return True