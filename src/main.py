from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import todo, test, user


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(todo.rounter)
app.include_router(test.rounter)
app.include_router(user.router)


@app.get("/", status_code=200)
def health_check():
    return {"ping": "pong"}
