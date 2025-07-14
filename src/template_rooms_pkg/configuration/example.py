from loguru import logger


def demo_config():
    logger.debug("Template rooms package - Demo configuration loaded successfully!")
    return {"status": "configured", "type": "template"}