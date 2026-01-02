

from fastapi import APIRouter,Request,HTTPException,status

from .auth import get_current_user,db_dependency
from models import Todos
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse

templates=Jinja2Templates('templates')
router=APIRouter(prefix='/todos',tags=['todos'])

class TodoRequest(BaseModel):
    title:str
    description:str
    priority:int
    complete:bool

@router.get('/todo-page')
async def render_todo_page(request:Request,db:db_dependency):
    try:
        print('calling render todo')
        access_token=request.cookies.get('access_token')
        user=await get_current_user(access_token)
        print(user,'-------------')
        if user is None:
            return redirect_to_login()
        user_id=user.get('id')
        todo_model=db.query(Todos).filter(Todos.owner_id==user_id).all()
        return templates.TemplateResponse('todo-page.html',{'request':request,'todos':todo_model,'user':user})
    except:
        return redirect_to_login()
@router.get('/add-todo-page')
async def render_add_todo_page(request:Request,db:db_dependency):
    access_token = request.cookies.get('access_token')
    user = await get_current_user(access_token)
    if user is None:
        return redirect_to_login()
    return templates.TemplateResponse('add-todo.html',{'request':request,'user':user})

@router.get('/edit-todo/{todo_id}')
async def render_add_todo_page(request:Request,db:db_dependency,todo_id:int):
    access_token = request.cookies.get('access_token')
    user = await get_current_user(access_token)
    if user is None:
        return redirect_to_login()
    todo_model=db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No such todo')

    return templates.TemplateResponse('edit-todo.html',{'todo':todo_model,'request':request, 'user':user})

def redirect_to_login():
    redirect_res=RedirectResponse(url='/auth/login',status_code=status.HTTP_302_FOUND)
    redirect_res.delete_cookie("access_token")
    return redirect_res


#-------------------------------ENDPOINTS--------------

@router.post('/add-todo',status_code=status.HTTP_201_CREATED)
async def write_todo(request:Request,todo_request:TodoRequest,db:db_dependency):
    access_token=request.cookies.get('access_token')
    user= await get_current_user(access_token)
    print(user)
    if user is None:
        return redirect_to_login()
    todo_model=Todos(title=todo_request.title,
                     description=todo_request.description,
                     complete=todo_request.complete,
                     priority=todo_request.priority,
                     owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

class UpdateTodo(BaseModel):
    id:int
    title:str
    description:str
    priority:int
    complete:bool

@router.post('/update-todo')
async def update_todo(updatetodo:UpdateTodo,request:Request,db:db_dependency):
    access_token = request.cookies.get('access_token')
    user = await get_current_user(access_token)
    if user is None:
        return redirect_to_login()
    todo_model=db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==updatetodo.id).first()
    todo_model.title=updatetodo.title
    todo_model.description=updatetodo.description
    todo_model.priority=updatetodo.priority
    todo_model.complete=updatetodo.complete
    db.add(todo_model)
    db.commit()

@router.delete('/delete-todo/{todo_id}')
async def delete_todo_from_url(request:Request,db:db_dependency,todo_id:int):
    access_token = request.cookies.get('access_token')
    user = await get_current_user(access_token)
    if user is None:
        return redirect_to_login()
    todo_model=db.query(Todos).filter(Todos.owner_id==user.get('id')).filter(Todos.id==todo_id).first()
    db.delete(todo_model)
    db.commit()



