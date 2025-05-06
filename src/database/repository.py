from typing import List

from fastapi import Depends, UploadFile, File
from database.connection import get_db
from sqlalchemy import select, delete, text
from sqlalchemy.orm import Session
from database.orm import Todo, User
from schema.request import FileUpload
from dotenv import load_dotenv
import os, time

load_dotenv(dotenv_path="D:/fastapi_leanning/.venv/pyvenv.cfg")


## dependency injection 예시 , 연쇠적으로 dependency injection 적용완료
class TodoRepository:
    UPLOAD_DIR = os.environ["UPLOAD_DIR"]

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
        select b.id , a.USERNAME , B.CONTENTS ,is_done , user_id
        from userm a , todo b
        WHERE 1 = 1
        AND A.ID = B.USER_ID
        order by 1 
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

    # 프로시저 호출
    def queryTest2(self):
        result = self.session.execute(
            text("BEGIN pkg_todo.get_all_todos(:cursor); END;"),
            {"cursor": self.session.bind.raw_connection().cursor()},
        )

        # 커서에서 결과 추출
        cursor = result.context.compiled_parameters[0]["cursor"]
        rows = cursor.fetchall()
        todo_list = [
            dict(zip([col[0] for col in cursor.description], row)) for row in rows
        ]

        return {"todos": todo_list}

    # 단순 파일 업로드
    def upload_file(
        self, fileObj: FileUpload, UploadFile: UploadFile | None = File(None)
    ) -> str:
        signal = "fail"
        user_dir = f"{self.UPLOAD_DIR}/{fileObj.w_id}/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        print(fileObj)

        filename_only, ext = os.path.splitext(fileObj.file_name)
        upload_filename = f"{filename_only}_{(int)(time.time()/1000)}.{ext}"
        upload_file_loc = user_dir + upload_filename
        with open(upload_file_loc, "wb") as outfile:
            while content := UploadFile.file.read(1024):
                outfile.write(content)
        print("upload successed", upload_file_loc)
        signal = "successed"
        return signal


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_user(self, user: User):
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def get_User_by_username(self, username: str) -> User | None:

        return self.session.scalar(select(User).where(User.username == username))
