from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base , relationship

from schema.request import CreateToDoRequest

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    model_config = ConfigDict(orm_mode=True)

    def __repr__(self):
        return f"todo(id = {self.id} , contents = {self.contents} , is_done = {self.is_done})"

    @classmethod
    def create(cls, request: CreateToDoRequest) -> "Todo":
        return cls(
            id=request.id,
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self) -> "Todo":
        self.is_done = "true"
        return self

    def undone(self) -> "Todo":
        self.is_done = "False"
        return self


class User(Base):

    __tablename__ = "userm"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship("Todo" , lazy="joined")
    
    @classmethod
    def create(cls , id: int, username: str , hashed_password: str) -> "User":
        return cls(
            id=id,
            username=username,
            password=hashed_password,
        )