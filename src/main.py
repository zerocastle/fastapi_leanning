from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo , delete_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSechema, ToDoSchema

app = FastAPI()

@app.get("/")
def health_check():
    return {"ping": "pong"}


@app.get("/todos" , status_code=200)
def get_todos_handler(order : str | None = None
                      , session : Session = Depends(get_db)
                      ) -> ToDoListSechema:
    todos:List[Todo]  = get_todos(session=session)

    if order == "DESC":
        return ToDoListSechema(
            todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    else:

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


@app.post("/todos" , status_code=201)
def post_todo_handler(
        request : CreateToDoRequest,
        session : Session = Depends(get_db)
) -> ToDoSchema:
    todo : Todo = Todo.create(request = request)
    todo : Todo = create_todo(sessoin=session , todo = todo)
    return ToDoSchema.model_validate(todo)


@app.patch("/todos/{todo_id}")
def path_todo_handler(
        todo_id : int ,
        is_done : bool = Body(... , embed=True),
        session : Session = Depends(get_db),
):
    todo : Todo | None = get_todo_by_todo_id(session=session , todo_id= todo_id)

    todo.done() if is_done else todo.undone()
    todo: Todo = update_todo(session, todo)
    return ToDoSchema.model_validate(todo)

@app.delete("/todos/{todo_id}" , status_code=204)
def delete_todo_handler(
        todo_id : int,
        session : Session = Depends(get_db)
):
    todo : Todo | None = get_todo_by_todo_id(session = session, todo_id= todo_id)
    if todo:
        delete_todo(session = session , todo_id = todo_id)
    raise HTTPException(status_code=404 , detail="ToDo Not Found")






