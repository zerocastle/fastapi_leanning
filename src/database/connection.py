import os
import cx_Oracle
from sqlalchemy import create_engine , text , select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:/fastApiLec/.venv/pyvenv.cfg")

username = os.environ['DB_ID']
password = os.environ['DB_PW']
hostname = os.environ['DB_URL']
port = os.environ['DB_PORT']
serviceNm = os.environ['DB_SERVICE_NM']

oracle_connection_string = f'oracle+cx_oracle://{username}:{password}@{hostname}:{port}?service_name={serviceNm}'

engine = create_engine(oracle_connection_string , echo=True)

with engine.connect() as conn:
    print(conn.scalar(text("select 1 from dual")))
    
SessionFactory = sessionmaker(autocommit=False, autoflush=False , bind=engine)


# generator 사용
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()



