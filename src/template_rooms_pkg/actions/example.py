from loguru import logger
from typing import Optional

from .base import ActionResponse, OutputBase, TokensSchema


class ActionOutput(OutputBase):
    message: str
    data: Optional[dict] = None


# entrypoint is always the same name as the action file name.
# the script use the function name, to simplify we will use the same name as the file.
def example() -> ActionResponse:
    logger.debug("Template rooms package - Example action executed successfully!")
    tokens = TokensSchema(stepAmount=2000, totalCurrentAmount=16236)
    output = ActionOutput(data={"foo": "bar"})
    message = "Action executed successfully"
    return ActionResponse(output=output, tokens=tokens, message=message)
