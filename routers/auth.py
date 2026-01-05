import os
import datetime
from datetime import timedelta,datetime,timezone
from http.client import HTTPException

from fastapi import APIRouter,Request,Depends,status,HTTPException
from fastapi.templating import Jinja2Templates
from pydantic.v1 import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated

from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt,JWTError
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

SECRET_KEY='3de5257449380335e0d6428367f0bbbe533f6d3c5b67180030ae085820254169'
ALGORITHM='HS256'

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

router=APIRouter(prefix='/auth',tags=['auth'])
templates=Jinja2Templates('templates')

class Register(BaseModel):
    email:str
    username:str
    password:str
    first_name:str
    last_name:str
    phone_number:str
    role:str
    is_active:bool

class Token(BaseModel):
    access_token:str
    token_type:str


@router.get('/login')
async def render_login_page(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.get('/register')
async def render_register_page(request:Request):
    return templates.TemplateResponse('register.html',{'request':request})

@router.get('/page')
async def get_cookie_value(request:Request):
    cookie=request.cookies.get('access_token')
    await get_current_user(cookie)
    return True

#api endpoints==================================================================

@router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:Register):
    user_model=Users(username=create_user_request.username,
                     hashed_password=bcrypt_context.hash(create_user_request.password),
                     first_name=create_user_request.first_name,
                     last_name=create_user_request.last_name,
                     role=create_user_request.role,
                     is_active=True,
                     phone_number=create_user_request.phone_number,
                     email=create_user_request.email
                    )
    db.add(user_model)
    db.commit()

@router.post('/token',status_code=status.HTTP_200_OK,response_model=Token)
async def create_token(login_form:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    authenticated=authenticate_user(login_form.username,login_form.password,db)
    if authenticated:
        token=create_access_token(authenticated.username,authenticated.role,authenticated.id,timedelta(minutes=20))
        return {'access_token':token,'token_type':'bearer'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Error creating token')

def authenticate_user(username:str,password:str,db:db_dependency):
    user_model=db.query(Users).filter(Users.username==username).first()
    if not user_model:
        return False
    correct_password=bcrypt_context.verify(password,user_model.hashed_password)
    if not correct_password:
        return False
    return user_model

def create_access_token(username:str,role:str,id:int,delta:timedelta):
    encode={'sub':username,'id':id,'role':role}
    expiry=datetime.now(timezone.utc)+delta
    encode.update({'exp':expiry})
    return_token=jwt.encode(encode,SECRET_KEY,ALGORITHM)
    return return_token


async def get_current_user(token:str):
    payload=jwt.decode(token=token,key=SECRET_KEY,algorithms=ALGORITHM)
    username=payload.get('sub')
    id=payload.get('id')
    role=payload.get('role')
    if username is None or id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='No such user')
    return {'username':username,'id':id, 'role':role}
