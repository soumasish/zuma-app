from sqlmodel import Session
from sqlalchemy import create_engine


engine = create_engine(
    "sqlite:///zuma.db", connect_args={"check_same_thread": False}, echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
