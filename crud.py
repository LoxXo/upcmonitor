import schemas
import models
from database import SessionLocal


def create_downstreamdata(db: SessionLocal, downstream: models.ChannelDataDown, entry_id_new: int) -> None:
    """Creates a new `.ChannelDataDownOrm` instance and adds it to the `Session`."""
    db_downstream = schemas.ChannelDataDownOrm(**downstream.dict(), entry_id=entry_id_new)
    db.add(db_downstream)


def create_upstreamdata(db: SessionLocal, upstream: models.ChannelDataUp, entry_id_new: int) -> None:
    """Creates a new `.ChannelDataUpOrm` instance and adds it to the `Session`."""
    db_upstream = schemas.ChannelDataUpOrm(**upstream.dict(), entry_id=entry_id_new)
    db.add(db_upstream)


def create_entrydata(db: SessionLocal, entry: models.EntryData) -> schemas.EntryDataOrm:
    """Creates a new `.EntryDataOrm` instance, adds it to the `Session` and flushes all changes to the database."""
    db_entry = schemas.EntryDataOrm(**entry.dict())
    db.add(db_entry)
    db.flush()
    return db_entry
