from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import TodoRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSechema, ToDoSchema

rounter = APIRouter(prefix="/todos")


@rounter.get("", status_code=200)
def get_todos_handler(
    order: str | None = None, todo_repo: TodoRepository = Depends(TodoRepository)
) -> ToDoListSechema:
    todos: List[Todo] = todo_repo.get_todos()

    if order == "DESC":
        return ToDoListSechema(
            todos=[ToDoSchema.model_validate(todo) for todo in todos[::-1]]
        )
    else:

        return ToDoListSechema(
            todos=[ToDoSchema.model_validate(todo) for todo in todos]
        )


@rounter.get("/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int, todo_repo: TodoRepository = Depends(TodoRepository)
) -> ToDoSchema:

    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        return ToDoSchema.model_validate(todo)
    raise HTTPException(status_code=404, detail="Todo not found !")


@rounter.post("", status_code=201)
def post_todo_handler(
    request: CreateToDoRequest, todo_repo: TodoRepository = Depends(TodoRepository)
) -> ToDoSchema:
    todo: Todo = Todo.create(request=request)
    todo: Todo = todo.create_todo(todo=todo)
    return ToDoSchema.model_validate(todo)


@rounter.patch("/{todo_id}")
def path_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: TodoRepository = Depends(TodoRepository),
):
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    todo.done() if is_done else todo.undone()
    todo: Todo = todo_repo.update_todo(todo)
    return ToDoSchema.model_validate(todo)


@rounter.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int, todo_repo: TodoRepository = Depends(TodoRepository)
):
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        todo_repo.delete_todo(todo_id=todo_id)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

