from sqlalchemy import create_engine, pool
from sqlalchemy.orm import scoped_session, sessionmaker

from . import settings
from .models import Base

def create_db():
    db_engine = create_engine(
        settings.DB_URL,
        poolclass=pool.NullPool,
        convert_unicode=True,
        connect_args={
            'application_name': settings.APP_NAME
        }
    )

    db_session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine
    ))

    Base.query = db_session.query_property()

    return db_engine, db_session


db_engine, db_session = create_db()
