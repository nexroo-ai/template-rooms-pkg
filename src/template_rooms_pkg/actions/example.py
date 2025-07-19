from loguru import logger
from typing import Optional
from pydantic import BaseModel

from .base import ActionResponse, OutputBase, TokensSchema
from template_rooms_pkg.configuration import CustomAddonConfig

class ActionInput(BaseModel):
    param1: str
    param2: str

class ActionOutput(OutputBase):
    message: str
    data: Optional[dict] = None
    code: Optional[int] = None

# entrypoint is always the same name as the action file name.
# the script use the function name, to simplify we will use the same name as the file.
def example(config: CustomAddonConfig, inputs: ActionInput) -> ActionResponse:
    if not isinstance(inputs, ActionInput):
        raise ValueError("Invalid input type. Expected ActionInput.")
    logger.info("Template rooms package - Example action executed successfully!")
    logger.info(f"Input received: {inputs}")
    logger.info(f"Config: {config}")
    # example of return response to fit the ActionResponse model
    tokens = TokensSchema(stepAmount=2000, totalCurrentAmount=16236)
    message = "Action executed successfully"
    code = 200
    output = ActionOutput(message=message, data={"foo": "bar"}, code=code)
    return ActionResponse(output=output, tokens=tokens)
