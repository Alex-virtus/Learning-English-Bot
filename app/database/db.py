from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from app.database.config import DSN

engine = create_engine(DSN, echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


def get_session():
    return SessionLocal()
