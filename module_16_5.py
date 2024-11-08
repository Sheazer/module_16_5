from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

users = []

templates = Jinja2Templates(directory='templates')

class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html',
                                      {'request': request, 'user': next((user for user in users if user.id == user_id), None)})


@app.post('/user/{username}/{age}')
async def create_user(user: User) -> User:
    if len(users) == 0:
        user.id = 1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    return user


@app.put('/user/{user_id}')
async def update_user(user_id: int, message: User) -> User:
    for i, user in enumerate(users):
        if user_id == user.id:
            users[i] = message
            users[i].id = user_id
            return users[i]
    raise HTTPException(status_code=404, detail="Message not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    for i, user in enumerate(users):
        if user_id == user.id:
            del users[i]
            return user
    raise HTTPException(status_code=404, detail="Message not found")
