

from fastapi import APIRouter,Request,HTTPException,status

from .auth import get_current_user,db_dependency
from models import Todos
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates('templates')
router=APIRouter(prefix='/todos',tags=['todos'])

@router.get('/todo-page')
async def render_todo_page(request:Request,db:db_dependency):
    access_token=request.cookies.get('access_token')
    user=await get_current_user(access_token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='No such user')
    user_id=user.get('id')
    todo_model=db.query(Todos).filter(Todos.owner_id==user_id).all()
    print(todo_model)
    return templates.TemplateResponse('todo-page.html',{'request':request,'todos':todo_model,'user':user})

