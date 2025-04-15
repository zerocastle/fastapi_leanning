from pydantic import BaseModel

from typing import List


class ToDoSchema(BaseModel):
    id : int
    contents : str
    is_done : str

    class Config:
        from_attributes = True

class ToDoListSechema(BaseModel):
    todos: List[ToDoSchema]
    

class UserShema(BaseModel):
    id : int
    username : str
    
    class Config:
        from_attributes = True
        
class JWTResponse(BaseModel):
    access_token: str