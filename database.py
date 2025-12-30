from sqlalchemy import create_engine,StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_DATABASE_URL='sqlite:///./todoapp2.db'
engine=create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False},poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
