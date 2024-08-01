import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"mysql+pymysql://admin:alberto05@bazar.c36mijirazht.us-east-1.rds.amazonaws.com/seller"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

DATABASE_URL_USER = f"mysql+pymysql://admin:alberto05@bazar.c36mijirazht.us-east-1.rds.amazonaws.com/user"
engine_user = create_engine(DATABASE_URL_USER)
SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_user)
BaseUser = declarative_base()