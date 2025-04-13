from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import TodoRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSechema, ToDoSchema
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="D:/fastApi/fastapi_leanning/.venv/pyvenv.cfg")
rounter = APIRouter(prefix="/test")
open_api_key = os.environ["OPEN_AI_API_KEY"]

client = OpenAI(api_key=open_api_key)


@rounter.get("", status_code=200)
def get_todos_handler(todo_repo: TodoRepository = Depends(TodoRepository)):
    result = todo_repo.queryTest()

    llm_query = f"""
                다음은 todo 목록입니다:
                {result}
                
                이 목록을 10개 행으로 복사 해주세요.
                """

    # print(llm_query)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "한글로 답해주세요."},
            {"role": "user", "content": llm_query},
        ],
    )

    result = response.choices[0].message.content

    return {"res": result}
