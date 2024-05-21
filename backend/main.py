from fastapi import FastAPI, HTTPException
# for cross origin resource sharing
from fastapi.middleware.cors import CORSMiddleware
from model import Todo

# app object
app = FastAPI()

# import functions from the database module
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)

# the frontend runs on port 3000, backend on port 8000
origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# perform all CRUD operations

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title: str):
    response = await fetch_one_todo(title)
    # handle exceptions
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"There is no TODO item with this title: {title}")

# it is a JSON, we have to convert it to a dictionary
@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(status_code=400, detail="Something went wrong / Bad Request")

# change the data of that todo id
@app.put("/api/todo/{title}/", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"There is no TODO item with this title: {title}")

# delete a todo
@app.delete("/api/todo/{title}")
async def delete_todo(title: str):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo item!"
    raise HTTPException(status_code=404, detail=f"There is no TODO item with this title: {title}")
