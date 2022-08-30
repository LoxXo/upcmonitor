from sqlalchemy.orm import Session
import schemas
import models


def create_downstreamdata(db: Session, downstream: schemas.ChannelDataDown, entry_id_new: int):
    db_downstream = models.ChannelDataDownOrm(**downstream.dict(), entry_id=entry_id_new)
    db.add(db_downstream)
    db.commit()
    db.refresh(db_downstream)
    return db_downstream


def get_downstreamdata_by_id(db: Session, id: int):
    return db.query(models.ChannelDataDownOrm).filter(models.ChannelDataDownOrm.id == id).first()


def get_downstreamdata(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChannelDataDownOrm).offset(skip).limit(limit).all()


def create_upstreamdata(db: Session, upstream: schemas.ChannelDataUp, entry_id_new: int):
    db_upstream = models.ChannelDataUpOrm(**upstream.dict(), entry_id=entry_id_new)
    db.add(db_upstream)
    db.commit()
    db.refresh(db_upstream)
    return db_upstream


def get_upstreamdata_by_id(db: Session, id: int):
    return db.query(models.ChannelDataUpOrm).filter(models.ChannelDataUpOrm.id == id).first()


def get_upstreamdata(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChannelDataUpOrm).offset(skip).limit(limit).all()


def create_entrydata(db: Session, entry: schemas.EntryData):
    db_entry = models.EntryDataOrm(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def get_entrydata_by_id(db: Session, entry_id: int):
    return db.query(models.EntryDataOrm).filter(models.EntryDataOrm.id == entry_id).first()


def get_entrydata(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EntryDataOrm).offset(skip).limit(limit).all()


def delete_entrydata_by_smh():
    pass
