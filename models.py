from datetime import datetime
from typing_extensions import Literal

from pydantic import BaseModel


class EntryData(BaseModel):
    timestamp: datetime


class ChannelDataDown(BaseModel):
    receiver_id: int
    channel_id: int
    lock_status: Literal['Locked', 'Unlocked']
    frequency: int
    modulation: str
    symbol_rate: int
    snr: float
    power: float


class ChannelDataUp(BaseModel):
    transmitter_id: int
    channel_id: int
    lock_status: Literal['Locked', 'Unlocked']
    frequency: int
    modulation: str
    symbol_rate: int
    channel_type: str
    power: float
