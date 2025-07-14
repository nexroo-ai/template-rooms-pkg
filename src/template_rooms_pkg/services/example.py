"""Example service for template rooms package."""

from loguru import logger


def demo_service():
    """Demo service function that prints a simple message."""
    logger.debug("Template rooms package - Demo service started successfully!")
    return {"service": "running", "port": 8080}