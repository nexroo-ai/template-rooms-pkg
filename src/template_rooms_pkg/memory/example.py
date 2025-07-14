"""Example memory for template rooms package."""

from loguru import logger


def demo_memory():
    """Demo memory function that prints a simple message."""
    logger.debug("Template rooms package - Demo memory system initialized successfully!")
    return {"memory_status": "active", "entries": 0}