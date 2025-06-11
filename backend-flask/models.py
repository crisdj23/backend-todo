import os
from peewee import *
from dotenv import load_dotenv

load_dotenv()
db = PostgresqlDatabase(None)

def init_db():
    db.init(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT'))
    )

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    title = CharField()
    done = BooleanField(default=False)