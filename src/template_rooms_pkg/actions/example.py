"""Example action for template rooms package."""

from loguru import logger


def demo_action():
    """Demo action function that prints a simple message."""
    logger.debug("Template rooms package - Demo action executed successfully!")
    return "Action completed"