import os

from fastapi import FastAPI, Request, status
from starlette.staticfiles import StaticFiles

from routers import auth
from routers import todos
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse



app=FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

templates=Jinja2Templates(directory='templates')

app.mount('/static',StaticFiles(directory="static"),name='static')

def redirect_to_todo():
    redirect_res=RedirectResponse('/todos/todo-page',status_code=status.HTTP_302_FOUND)
    return redirect_res

@app.get('/')
async def all_ok(request:Request):
    return redirect_to_todo()