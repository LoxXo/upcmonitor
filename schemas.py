from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class EntryDataOrm(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    timestamp = Column(DateTime, nullable=False)
    downstream = relationship('ChannelDataDownOrm', back_populates='entry')
    upstream = relationship('ChannelDataUpOrm', back_populates='entry')


class ChannelDataDownOrm(Base):
    __tablename__ = 'downstream'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    receiver_id = Column(Integer)
    channel_id = Column(Integer)
    lock_status = Column(String(8))
    frequency = Column(Integer)
    modulation = Column(String(7))
    symbol_rate = Column(Integer)
    snr = Column(Float)
    power = Column(Float)
    entry_id = Column(Integer, ForeignKey('entry.id'), nullable=False)

    entry = relationship('EntryDataOrm', back_populates='downstream')


class ChannelDataUpOrm(Base):
    __tablename__ = 'upstream'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    transmitter_id = Column(Integer)
    channel_id = Column(Integer)
    lock_status = Column(String(8))
    frequency = Column(Integer)
    modulation = Column(String(7))
    symbol_rate = Column(Integer)
    channel_type = Column(String(5))
    power = Column(Float)
    entry_id = Column(Integer, ForeignKey('entry.id'), nullable=False)

    entry = relationship('EntryDataOrm', back_populates='upstream')
