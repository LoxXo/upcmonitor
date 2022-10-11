from sqlalchemy import create_engine, event, exc
from sqlalchemy.orm import sessionmaker

from schemas import Base

# set database URL like 'dialect+driver://username:password@host:port/database'
_SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://upcmonitor:upcmonitor123@192.168.43.5:5432/upc'

# name of PostgreSQL schema
_SCHEMA_NAME = 'upclive'

_engine = create_engine(
    _SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
sessionlocal = SessionLocal()


@event.listens_for(_engine, 'connect', insert=True)
def set_search_path(dbapi_connection, connection_record):
    """Configurates schema for every transaction in connection."""
    print('Setting session search path')
    existing_autocommit = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor = dbapi_connection.cursor()
    cursor.execute(f'SET SESSION search_path="{_SCHEMA_NAME}"')
    cursor.close()
    dbapi_connection.autocommit = existing_autocommit


def create_tables():
    """Checks for tables and if not present create them."""
    try:
        Base.metadata.create_all(_engine)
    except exc.OperationalError as sqlerr:
        raise SystemExit('Database connection error.', sqlerr)
