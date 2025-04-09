from fastapi.testclient import TestClient
from main import app
from schema.response import ToDoSchema
from database.orm import Todo

client = TestClient(app = app)


# def test_health_check(mocker) :
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"ping": "pong"}


#실제 메서드를 호출하여 데이터를 불러오는게 아닌 가 데이터를 만들어 놓는것
def get_todos_handler(mocker):
    mocker.patch("main.get_todos_handler", return_value=[
        Todo(id = 1 , contents="lalalal" , is_done="True"),
        Todo(id=2, contents="현우씨 코그모", is_done="False"),
    ])

    response = client.get("/todos")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "todos" : [
            {"id" : 1 , "contents" : "lalalal" , "is_done" : "True"},
            {"id" : 2 , "contents" : "현우씨 코그모" , "is_done" : "False"},
        ]
    }

# def get_todo_handler(mocker):
#     mocker.patch("main.requests.get")
#
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"ping": "pong"}