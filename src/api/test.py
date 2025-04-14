from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from database.orm import Todo
from database.repository import TodoRepository

from openai import OpenAI
from dotenv import load_dotenv
import os
from schema.request import  requestLLM


load_dotenv(dotenv_path="D:/fastApiLec/.venv/pyvenv.cfg")
rounter = APIRouter(prefix="/testLLM")
open_api_key = os.environ["OPEN_AI_API_KEY"]

client = OpenAI(api_key=open_api_key)


@rounter.post("", status_code=200)
def post_todos_handler(
                        request_data : requestLLM ,
                        todo_repo: TodoRepository = Depends(TodoRepository)
                       
                       ):
    result = todo_repo.queryTest()

    llm_query = f"""
                다음은 todo 목록입니다 아래 있는 참고 사항과 사용자 질의를 보고 답변해 주세요.:
                {result}
                
                #참고 사항 
                 - is_done 1은 완료 된 상태이고 0은 완료 되지 못한 상태 입니다.
                
                #사용자의 질문 : {request_data.question}
                
                """

    # print(llm_query)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "한글로 답해주세요."},
            {"role": "user", "content": llm_query},
        ],
    )

    result = response.choices[0].message.content

    return {"res": result}
