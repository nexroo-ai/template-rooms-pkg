"""Example tool for template rooms package."""

from loguru import logger


def demo_tool():
    """Demo tool function that prints a simple message."""
    logger.debug("Template rooms package - Demo tool executed successfully!")
    return {"tool": "template_tool", "result": "success"}