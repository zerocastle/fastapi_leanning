from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todo"
    
    id = Column(Integer , primary_key=True , index = True)
    contents = Column(String(256), nullable=False)
    is_done = Column(String , nullable=False)
        
    def __repr__(self):
        return f"todo(id = {self.id} , contents = {self.contents} , is_done = {self.is_done})"

