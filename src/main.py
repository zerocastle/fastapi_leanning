from typing import List
from fastapi import FastAPI
from api import todo, test

app = FastAPI()
app.include_router(todo.rounter)
app.include_router(test.rounter)


@app.get("/", status_code=200)
def health_check():
    return {"ping": "pong"}
