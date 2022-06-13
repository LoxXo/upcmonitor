from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing_extensions import Literal


class ChannelDataDown(BaseModel):
    receiver_id: int
    channel_id: int
    lock_status: Literal["Locked", "Unlocked"]
    frequency: int
    modulation: str
    symbol_rate: int
    snr: float
    power: float


class ChannelDataUp(BaseModel):
    transmitter_id: int
    channel_id: int
    lock_status: Literal["Locked", "Unlocked"]
    frequency: int
    modulation: str
    symbol_rate: int
    channel_type: str
    power: float


def scrap_downstream(html_down: str):
    soup_down = BeautifulSoup(html_down, "lxml")
    downchannels_data = list()

    tbody = soup_down.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        receiver_id = tds[0].text
        channel_id = tds[1].text

        lock = tds[2]
        lock_raw = lock.find("script").text
        lock_raw = lock_raw.lstrip('i18n("').rstrip('")')
        if lock_raw == "TAG_UPC_T38":
            lock_raw = "Locked"
        if lock_raw == "TAG_UPC_T39":
            lock_raw = "Unlocked"

        frequency = tds[3].text

        modulation = tds[4]
        modulation_raw = modulation.find("script").text
        modulation_raw = modulation_raw.lstrip('i18n("').rstrip('")')

        rate = tds[5]
        symbol_raw = rate.find("script").text
        symbol_raw = symbol_raw.lstrip('i18n("').rstrip('")')

        snr = tds[6].text

        power = tds[7].text

        downchannels_data.append(
            ChannelDataDown(
                receiver_id=receiver_id,
                channel_id=channel_id,
                lock_status=lock_raw,
                frequency=frequency,
                modulation=modulation_raw,
                symbol_rate=symbol_raw,
                snr=snr,
                power=power,
            )
        )
    print(downchannels_data)

    return downchannels_data


def scrap_upstream(html_up: str):
    soup_up = BeautifulSoup(html_up, "lxml")
    upchannels_data = list()

    tbody = soup_up.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        transmitter_id = tds[0].text
        channel_id = tds[1].text

        lock = tds[2]
        lock_raw = lock.find("script").text
        lock_raw = lock_raw.lstrip('i18n("').rstrip('")')
        if lock_raw == "TAG_UPC_T38":
            lock_raw = "Locked"
        if lock_raw == "TAG_UPC_T39":
            lock_raw = "Unlocked"

        frequency = tds[3].text

        modulation = tds[4]
        modulation_raw = modulation.find("script").text
        modulation_raw = modulation_raw.lstrip('i18n("').rstrip('")')

        symbol_rate = tds[5].text

        channel_type = tds[6]
        channel_type_raw = channel_type.find("script").text
        channel_type_raw = channel_type_raw.lstrip('i18n("').rstrip('")')

        power = tds[7].text

        upchannels_data.append(
            ChannelDataUp(
                transmitter_id=transmitter_id,
                channel_id=channel_id,
                lock_status=lock_raw,
                frequency=frequency,
                modulation=modulation_raw,
                symbol_rate=symbol_rate,
                channel_type=channel_type_raw,
                power=power,
            )
        )
    print(upchannels_data)
    return upchannels_data
