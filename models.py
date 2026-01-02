from database import Base,engine
from sqlalchemy import Integer,String,Column,Boolean,ForeignKey, MetaData

class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True)
    email=Column(String,unique=True)
    first_name=Column(String)
    last_name=Column(String)
    phone_number=Column(String)
    is_active=Column(Boolean)
    hashed_password=Column(String)
    role=Column(String)


class Todos(Base):
    __tablename__='todos'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    priority=Column(Integer)
    description=Column(String)
    complete=Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey('users.id'))
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
