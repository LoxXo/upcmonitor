import unittest
import pathlib
from scrapper import ChannelDataDown, ChannelDataUp, scrap_downstream, scrap_upstream


def get_html_content(filename: str) -> str:
    html_file = pathlib.Path(__file__).parent / "html" / filename

    print(html_file)
    with open(html_file, encoding="utf8") as f:
        return f.read()


class TestScraper(unittest.TestCase):
    def test_downstream(self):
        html = get_html_content("get_downstream.html")
        downstream_data = scrap_downstream(html)

        self.assertListEqual(
            downstream_data,
            [
                ChannelDataDown(
                    receiver_id=1,
                    channel_id=9,
                    lock_status="Locked",
                    frequency=738000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.4,
                    power=1.2,
                ),
                ChannelDataDown(
                    receiver_id=2,
                    channel_id=10,
                    lock_status="Locked",
                    frequency=746000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.8,
                    power=1.4,
                ),
                ChannelDataDown(
                    receiver_id=3,
                    channel_id=11,
                    lock_status="Locked",
                    frequency=754000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.8,
                    power=1.8,
                ),
                ChannelDataDown(
                    receiver_id=4,
                    channel_id=12,
                    lock_status="Locked",
                    frequency=762000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.9,
                    power=1.6,
                ),
                ChannelDataDown(
                    receiver_id=5,
                    channel_id=1,
                    lock_status="Locked",
                    frequency=674000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.8,
                    power=2.2,
                ),
                ChannelDataDown(
                    receiver_id=6,
                    channel_id=2,
                    lock_status="Locked",
                    frequency=682000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.8,
                    power=1.6,
                ),
                ChannelDataDown(
                    receiver_id=7,
                    channel_id=3,
                    lock_status="Locked",
                    frequency=690000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.3,
                    power=1.2,
                ),
                ChannelDataDown(
                    receiver_id=8,
                    channel_id=4,
                    lock_status="Locked",
                    frequency=698000000,
                    modulation="256QAM",
                    symbol_rate=6952000,
                    snr=40.3,
                    power=1.3,
                ),
            ],
        )

    def test_upstream(self):
        html = get_html_content("get_upstream.html")
        upstream_data = scrap_upstream(html)

        self.assertListEqual(
            upstream_data,
            [
                ChannelDataUp(
                    transmitter_id=1,
                    channel_id=9,
                    lock_status="Locked",
                    frequency=34300000,
                    modulation="64QAM",
                    symbol_rate=5120000,
                    channel_type="ATDMA",
                    power=42.0,
                ),
                ChannelDataUp(
                    transmitter_id=2,
                    channel_id=13,
                    lock_status="Locked",
                    frequency=61100000,
                    modulation="64QAM",
                    symbol_rate=5120000,
                    channel_type="ATDMA",
                    power=44.3,
                ),
                ChannelDataUp(
                    transmitter_id=3,
                    channel_id=11,
                    lock_status="Locked",
                    frequency=47700000,
                    modulation="64QAM",
                    symbol_rate=5120000,
                    channel_type="ATDMA",
                    power=42.5,
                ),
                ChannelDataUp(
                    transmitter_id=4,
                    channel_id=12,
                    lock_status="Locked",
                    frequency=54400000,
                    modulation="64QAM",
                    symbol_rate=5120000,
                    channel_type="ATDMA",
                    power=44.5,
                ),
            ],
        )
