from pydantic import BaseModel


class PromptDTO(BaseModel):
    user_input: str
    
class PromptMessagesDTO(BaseModel):
    messages: list
    