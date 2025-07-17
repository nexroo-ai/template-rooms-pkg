from loguru import logger
from typing import Optional

from .base import ActionResponse, OutputBase, TokensSchema

class ActionOutput(OutputBase):
    message: str
    data: Optional[dict] = None
    code: Optional[int] = None

# entrypoint is always the same name as the action file name.
# the script use the function name, to simplify we will use the same name as the file.
def example(param1: str, param2: str) -> ActionResponse:
    logger.debug("Template rooms package - Example action executed successfully!")
    logger.debug(f"Input received: {input}")
    tokens = TokensSchema(stepAmount=2000, totalCurrentAmount=16236)
    message = "Action executed successfully"
    code = 200
    output = ActionOutput(message=message, data={"foo": "bar"}, code=code)
    return ActionResponse(output=output, tokens=tokens)
