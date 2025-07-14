"""Template rooms package for AI rooms script."""

from loguru import logger


def test() -> bool:
    """Test function for template rooms package.
    
    Returns:
        bool: True if test passes, False otherwise
    """
    logger.info("Running template-rooms-pkg test...")
    
    # Simple test logic - always returns True for template
    logger.info("Template rooms package test passed")
    return True