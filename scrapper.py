import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from sqlalchemy import exc

import models
import database
import crud


# data source router's ip and login
_ROUTER_IP = '192.168.42.1'
_ROUTER_LOGIN = 'admin'
_ROUTER_PASSWORD = 'admin'

# 1 to make script log out any users from router panel during its login
_LOGOFF_USER = 0


def scrap_downstream(html_down: str) -> List[models.ChannelDataDown]:
    soup_down = BeautifulSoup(html_down, 'lxml')
    downchannels_data = list()

    tbody = soup_down.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        receiver_id = tds[0].text
        channel_id = tds[1].text

        lock = tds[2]
        lock_raw = lock.find('script').text
        lock_raw = lock_raw.lstrip('i18n("').rstrip('")')
        if lock_raw == 'TAG_UPC_T38':
            lock_raw = 'Locked'
        if lock_raw == 'TAG_UPC_T39':
            lock_raw = 'Unlocked'

        frequency = tds[3].text

        modulation = tds[4]
        modulation_raw = modulation.find('script').text
        modulation_raw = modulation_raw.lstrip('i18n("').rstrip('")')
        if modulation_raw == 'TAG_UPC_T37':
            modulation_raw = 'N/A'

        rate = tds[5]
        symbol_raw = rate.find('script').text
        symbol_raw = symbol_raw.lstrip('i18n("').rstrip('")')

        snr = tds[6].text

        power = tds[7].text

        downchannels_data.append(
            models.ChannelDataDown(
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
    return downchannels_data


def scrap_upstream(html_up: str) -> List[models.ChannelDataUp]:
    soup_up = BeautifulSoup(html_up, 'lxml')
    upchannels_data = list()

    tbody = soup_up.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        transmitter_id = tds[0].text
        channel_id = tds[1].text

        lock = tds[2]
        lock_raw = lock.find('script').text
        lock_raw = lock_raw.lstrip('i18n("').rstrip('")')
        if lock_raw == 'TAG_UPC_T38':
            lock_raw = 'Locked'
        if lock_raw == 'TAG_UPC_T39':
            lock_raw = 'Unlocked'

        frequency = tds[3].text

        modulation = tds[4]
        modulation_raw = modulation.find('script').text
        modulation_raw = modulation_raw.lstrip('i18n("').rstrip('")')
        if modulation_raw == 'TAG_UPC_T37':
            modulation_raw = 'N/A'

        symbol_rate = tds[5].text

        channel_type = tds[6]
        channel_type_raw = channel_type.find('script').text
        channel_type_raw = channel_type_raw.lstrip('i18n("').rstrip('")')
        if modulation_raw == 'TAG_UPC_T37':
            modulation_raw = 'N/A'

        power = tds[7].text

        upchannels_data.append(
            models.ChannelDataUp(
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
    return upchannels_data


def check_if_on_loginpage(url_check: str) -> None:
    # loginpage_str is a part of upc_loginform html class with login input fields
    loginpage_str_to_compare = '<h2><script>i18n("LOGIN_AREA_LABEL2=")</script></h2>'
    try:
        url_check_response = requests.get(url_check, timeout=10)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit('Router connection error', errc)
    loginpage = BeautifulSoup(url_check_response.text, 'lxml')
    check_loginpage = loginpage.find('h2')
    if (
        str(check_loginpage) == loginpage_str_to_compare
    ):
        print('Not logged in')
        login_into()


def login_into() -> None:
    print('Trying to login...')
    url_login = (f'http://{_ROUTER_IP}/goform/login')
    s = requests.get(f'http://{_ROUTER_IP}/login.asp')
    stx = BeautifulSoup(s.text, 'lxml')
    csrf = str(stx.find('input'))
    csrf = csrf.lstrip('<input name="CSRFValueL" type="hidden" value=').rstrip('"/>')
    print(f'CSRFValue={csrf}')
    login_payload = {
        'CSRFValue': f'{csrf}',
        'loginUsername': f'{_ROUTER_LOGIN}',
        'loginPassword': f'{_ROUTER_PASSWORD}',
        'logoffUser': f'{_LOGOFF_USER}',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': f'http://{_ROUTER_IP}',
        'Connection': 'keep-alive',
        'Referer': f'http://{_ROUTER_IP}',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Sec-GPC': '1',
    }
    logged_url = requests.post(url_login, data=login_payload, headers=headers)
    print(f'Logged in successfully with status: {logged_url.status_code}')


def request_downstream() -> str:
    url_downstream = f'http://{_ROUTER_IP}/status/connection-downstream.asp'
    print('Requesting data from downstream.asp...')
    response_down = requests.get(url_downstream, timeout=10)
    return response_down.text


def request_upstream() -> str:
    url_upstream = f'http://{_ROUTER_IP}/status/connection-upstream.asp'
    print('Requesting data from upstream.asp...')
    response_up = requests.get(url_upstream, timeout=10)
    return response_up.text


def create_entry() -> models.EntryData:
    entry_datetime = datetime.datetime.now(datetime.timezone.utc)
    return models.EntryData(timestamp=entry_datetime)


def transaction_full(downstream: List[models.ChannelDataDown], upstream: List[models.ChannelDataUp]):
    """Create and commit EntryData and ChannelDataUp/Down with relation by entry.id."""
    new_entry = create_entry()
    try:
        last_entry = crud.create_entrydata(database.sessionlocal, new_entry)
        for row_down in downstream:
            crud.create_downstreamdata(database.sessionlocal, row_down, last_entry.id)
        for row_up in upstream:
            crud.create_upstreamdata(database.sessionlocal, row_up, last_entry.id)
        database.sessionlocal.commit()
        print('All done!')
    except exc.SQLAlchemyError as sqlerr:
        database.sessionlocal.rollback()
        print('Commit error:', sqlerr)


if __name__ == '__main__':
    database.create_tables()
    check_if_on_loginpage(f'http://{_ROUTER_IP}/status/connection-downstream.asp')
    resp_down = request_downstream()
    down = scrap_downstream(resp_down)
    resp_up = request_upstream()
    up = scrap_upstream(resp_up)
    transaction_full(down, up)
