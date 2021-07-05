from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from typing import Optional



class TODO(BaseModel):
    Task:str
    Description:str

app = FastAPI(title='TODO API')
store_todo = []

@app.get('/')
async def home():
    return{"hello":'world'}

@app.post('/add_task/')
async def create(todo:TODO):
    store_todo.append(todo.dict())
    return store_todo

@app.get('/view_list/',response_model=list[TODO])
async def get_all_todo():
    return store_todo

@app.get('/get_task/{id}')
async def get_todo(id:int):
    try:
        return store_todo[id]
    except:
        raise HTTPException(status_code=404,detail='Todo not found')

@app.put('/Update_task/{id}')
async def update_todo(id:int,todo:TODO):
    try:
        store_todo[id] = todo
        return store_todo[id]
    except:
        raise HTTPException(status_code=404,detail='Todo not found')

@app.delete('/Delete_task/{id}')
async def delete_todo(id:int):
    try:
        obj = store_todo[id]
        store_todo.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404,detail='Todo not found')