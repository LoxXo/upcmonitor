from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing_extensions import Literal


class ChannelData(BaseModel):
    receiver_id: int
    channel_id: int
    lock_status: Literal["Locked", "Unlocked"]
    frequency: int
    modulation: str
    symbol_rate: int
    snr: float
    power: float


def scrap_downstream(html_down: str):
    soup_down = BeautifulSoup(html_down, "lxml")

    td_list = list()  # receiver id, channel id, frequency, snr, power
    script_list = list()  # lock status, modulation, symbol rate

    for td in soup_down.find_all("td"):
        td_list.append(td.text)
    tdx_list = [x for idx, x in enumerate(td_list) if td_list[idx] != "\n\n"]

    tbody = soup_down.find("tbody")
    rows = tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        id = tds[0].text
        channel = tds[1].text
        rate = tds[5]
        symbol_raw = rate.find("script").text
        symbol_raw.lstrip('i18n("').rstrip('")')


    script_tags = soup_down.find_all("script")
    script_tags = script_tags[34:58]
    for st in script_tags:
        st = st.text
        st = st.lstrip("i18n(")
        st = st.rstrip(")")
        script_list.append(
            st
        )  # todo translating TAG_UPC to text (only to unlocked/locked or from entire english.js?)

    # print(tdx_list)
    # print(script_list)

    return tdx_list


# soup_down.tbody.tr.script
