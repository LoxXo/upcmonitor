from typing import List
from bs4 import BeautifulSoup
import requests


def scrap_downstream(html_down):
    with open(html_down, "rb") as down:
        soup_down = BeautifulSoup(down, "lxml")

    td_list = list()  # receiver id, channel id, frequency, snr, power
    script_list = list()  # lock status, modulation, symbol rate

    for td in soup_down.find_all("td"):
        td_list.append(td.text)
    tdx_list = [x for idx, x in enumerate(td_list) if td_list[idx] != "\n\n"]

    script_tags = soup_down.find_all("script")
    script_tags = script_tags[34:58]
    for st in script_tags:
        st = st.text
        st = st.lstrip("i18n(")
        st = st.rstrip(")")
        script_list.append(
            st
        )  # todo translating TAG_UPC to text (only to unlocked/locked or from entire english.js?)

    print(tdx_list)
    print(script_list)


# soup_down.tbody.tr.script

scrap_downstream("get_downstream.html")
