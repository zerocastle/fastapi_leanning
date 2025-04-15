from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    id : int
    contents: str
    is_done: str



class requestLLM(BaseModel):
    question : str
    

# 유저 가입 , 인증 관련 pydantic

class SignUpRequest(BaseModel):
    id : int
    username : str
    password : str
    
class Login_by_user(BaseModel):
    username : str
    password : str
    
    