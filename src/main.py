from fastapi import FastAPI , Body , HTTPException
from pydantic import BaseModel
import json
app = FastAPI()

@app.get("/")
def health_check():
    return {"ping": "pong"}

todo_data = {
    1 : {
        "id" : 1,
        "content" : "실전 fastapi 섹션 수강 0",
        "is_done" : True,
    },
    2 : {
        "id" : 2,
        "content" : "실전 fastapi 섹션 수강 0",
        "is_done" : False,
    },
    3 : {
        "id" : 3,
        "content" : "실전 fastapi 섹션 수강 0",
        "is_done" : False,
    }

}

@app.get("/todos" , status_code=200)
def get_todos_handler(order : str | None = None):
    ref = list(todo_data.values())
    
    if order == "DESC":
        return ref[::-1]
    return ref

@app.get("/todos/{todo_id}" , status_code=200)
def get_todo_handler(todo_id : int):

    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404 , detail="Todo not found !")


class CreateRequest(BaseModel):
    id : int
    content: str
    is_done: bool

@app.post("/todos")
def post_todo_handler(request : CreateRequest):
    todo_data[request.id] = request.model_dump()
    return todo_data[request.id]


@app.patch("/todos/{todo_id}")
def path_todo_handler(
        todo_id : int ,
        is_done : bool = Body(... , embed=True),
):
    todo = todo_data.get(todo_id)

    if todo:
        todo["is_done"] = is_done
        return todo
    return {}

@app.delete("/todos/{todo_id}")
def delete_todo_handler(
        todo_id : int
):
    todo_data.pop(todo_id , None)
    return todo_data








