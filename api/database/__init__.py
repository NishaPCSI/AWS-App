from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# -------------------------------------Database URL Configuration---------------------------------------

SQLALCHEMY_DATABASE_URL = "postgresql://Group42_admin:Nisarg#123@group42-database.c5iq0gm14ozl.us-east-1.rds.amazonaws.com:5432/Group42_Database"

# -------------------------------------Engine Setup---------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# -------------------------------------Session and Base---------------------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
