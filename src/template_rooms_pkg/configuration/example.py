"""Example configuration for template rooms package."""

from loguru import logger


def demo_config():
    """Demo configuration function that prints a simple message."""
    logger.debug("Template rooms package - Demo configuration loaded successfully!")
    return {"status": "configured", "type": "template"}