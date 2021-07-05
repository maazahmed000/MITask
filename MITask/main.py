import os
import urllib

from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from typing import Optional

import databases, sqlalchemy
#DATABASE_URL = "sqlite:///./test.db"

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'fastapi')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'secret')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
TODO_Lists = sqlalchemy.Table(
    "py_TODO_Lists",
    metadata,
    sqlalchemy.Column("Tasks"        , sqlalchemy.String),
    sqlalchemy.Column("Description"  , sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
    # DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)

# store_todo=[]

class TODO(BaseModel):
    Task:str
    Description:str

app = FastAPI(title='TODO API')

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def startup():
    await database.disconnect()

@app.get('/')
async def home():
    return{"hello":'world'}

@app.post('/add_task/')
async def create(todo:TODO):
    # store_todo.append(todo.dict())
    query = TODO_Lists.insert().values(Task=TODO.Task, Description=TODO.Description)
    last_record_id = await database.execute(query)
    # return store_todo
    return (TODO.dict())


@app.get('/view_list/',response_model=list[TODO])
async def get_all_todo():
    # return store_todo
    return await database.fetch_all()

@app.get('/get_task/{id}')
async def get_todo(todo_id:int):
    try:
        # return store_todo[id]
        query = TODO.select().where(TODO.c.id == todo_id)
        return await database.fetch_one(query)
    except:
        raise HTTPException(status_code=404,detail='Todo not found')

@app.put('/Update_task/{id}')
async def update_todo(todo_id:int,todo:TODO):
    try:
        # store_todo[id] = todo
        # return store_todo[id]
        query = TODO.update().where(TODO.c.id == todo_id).values(text=todo.Task, completed=todo.Description)
        await database.execute(query)
        return {"message":"update done"}
    except:
        raise HTTPException(status_code=404,detail='Todo not found')

@app.delete('/Delete_task/{id}')
async def delete_todo(todo_id:int):
    try:
        # obj = store_todo[id]
        # store_todo.pop(id)
        # return obj
        query = TODO.delete().where(TODO.c.id == todo_id)
        await database.execute(query)
        return {"message": "Note with id: {} deleted successfully!".format(todo_id)}
    except:
        raise HTTPException(status_code=404,detail='Todo not found')
