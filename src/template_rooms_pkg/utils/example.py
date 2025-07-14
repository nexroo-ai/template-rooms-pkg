"""Example utility for template rooms package."""

from loguru import logger


def demo_util():
    """Demo utility function that prints a simple message."""
    logger.debug("Template rooms package - Demo utility function executed successfully!")
    return {"utility": "helper", "status": "ready"}