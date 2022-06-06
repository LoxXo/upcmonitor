import unittest
import pathlib
from scrapper import scrap_downstream


def get_html_content(filename: str) -> str:
    html_file = pathlib.Path(__file__).parent / "html" / filename

    print(html_file)
    with open(html_file) as f:
        return f.read()


class TestScraper(unittest.TestCase):
    def test_downstream(self):
        html = get_html_content("get_downstream.html")
        downstream_data = scrap_downstream(html)

        self.assertListEqual(
            downstream_data,
            [
                "1",
                "9",
                "738000000",
                "40.4",
                " 1.2",
                "2",
                "10",
                "746000000",
                "40.8",
                " 1.4",
                "3",
                "11",
                "754000000",
                "40.8",
                " 1.8",
                "4",
                "12",
                "762000000",
                "40.9",
                " 1.6",
                "5",
                "1",
                "674000000",
                "40.8",
                " 2.2",
                "6",
                "2",
                "682000000",
                "40.8",
                " 1.6",
                "7",
                "3",
                "690000000",
                "40.3",
                " 1.2",
                "8",
                "4",
                "698000000",
                "40.3",
                " 1.3",
            ],
        )
