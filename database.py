from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # or from sqlmodel import SQLModel

db_url = "postgresql://postgres:password@localhost:5432/fast_api_crud"
engine = create_engine(db_url)
session= sessionmaker(autocommit = False,autoflush=False,bind = engine)
Base = declarative_base() # or Base = SQLModel
Base.metadata.create_all(bind=engine)
