from typing import List

from fastapi import Depends
from database.connection import get_db
from sqlalchemy import select, delete, text
from sqlalchemy.orm import Session
from database.orm import Todo

## dependency injection 예시 , 연쇠적으로 dependency injection 적용완료


class TodoRepository:
    def __init__(self, sesssion: Session = Depends(get_db)):
        self.session = sesssion

    def get_todos(self) -> List[Todo]:
        return list(self.session.scalars(select(Todo)))

    def get_todo_by_todo_id(self, todo_id: int) -> Todo | None:
        return self.session.scalar(select(Todo).where(Todo.id == todo_id))

    def create_todo(self, todo: Todo) -> Todo:
        self.sessoin.add(instance=todo)
        self.sessoin.commit()
        self.sessoin.refresh(instance=todo)
        return todo

    def update_todo(self, todo: Todo) -> Todo:
        self.session.add(instance=todo)
        self.session.commit()
        self.session.refresh(instance=todo)
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(Todo).where(Todo.id == todo_id))
        self.session.commit()

    def queryTest(self):
        query = text(
            """
        select *
        from userm a , todo b
        where 1 = 1
        and a.id = b.id
        """
        )
        result = self.session.execute(query)
        # print(result)
        # 다건 조회
        rows = result.fetchall()
        todo_list = [dict(row._mapping) for row in rows]
        return {"todos": todo_list}
        # 단건 조회
        # row = result.fetchone()
        # todo = dict(row._mapping)
        # return {"todo" : todo}
