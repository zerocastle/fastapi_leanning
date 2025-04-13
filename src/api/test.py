from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import TodoRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSechema, ToDoSchema

rounter = APIRouter(prefix="/test")


@rounter.get("", status_code=200)
def get_todos_handler(todo_repo: TodoRepository = Depends(TodoRepository)):

    result = todo_repo.queryTest()

    return result

    # print(todo_repo.queryTest())
