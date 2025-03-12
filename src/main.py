from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id
from schema.request import CreateRequest
from schema.response import ToDoListSechema, ToDoSchema

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
def get_todos_handler(order : str | None = None
                      , session : Session = Depends(get_db)
                      ) -> ToDoListSechema:
    todos:List[Todo]  = get_todos(session=session)

    if order == "DESC":
        return ToDoListSechema(
       todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]]
    )
    return ToDoListSechema(
       todos=[ToDoSchema.model_validate(todo) for todo in todos]
    )

@app.get("/todos/{todo_id}" , status_code=200)
def get_todo_handler(todo_id : int
                     , session : Session = Depends(get_db)
                     ) ->ToDoSchema:

    todo : Todo | None = get_todo_by_todo_id(session = session , todo_id = todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404 , detail="Todo not found !")


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





