from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://upcmonitor:upcmonitor123@192.168.43.5:5432/upc"
schema_name = 'upclive'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


@event.listens_for(engine, "connect", insert=True)
def set_search_path(dbapi_connection, connection_record):
    print('setting session search path')
    existing_autocommit = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor = dbapi_connection.cursor()
    cursor.execute("SET SESSION search_path='%s'" % schema_name)
    cursor.close()
    dbapi_connection.autocommit = existing_autocommit


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
sessionlocal = SessionLocal()


# Checks for tables if not present create them.
def create_tables():
    Base.metadata.create_all(engine)
