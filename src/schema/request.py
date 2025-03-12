from pydantic import BaseModel


class CreateRequest(BaseModel):
    id : int
    content: str
    is_done: bool
