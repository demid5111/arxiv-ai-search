from functools import partial
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

from arxiv_scrapper.config_dto import Config
from arxiv_scrapper.parser import HTMLParser


def make_session(config: Config):
    session = requests.Session()

    retry = Retry(connect=2)
    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update(config.get_headers())
    session.request = partial(session.request, timeout=config.get_timeout())
    session.verify = False

    return session

def make_request(session, url) -> requests.models.Response:
    """
    Delivers a response from a request
    with given configuration
    """
    return session.get(url)


class TargetURL:
    base_template = 'https://arxiv.org/list/cs/{year}{month}?skip={cur_page_index}&show={max_links_per_page}'
    max_links_per_page = 2000
    def __init__(self, year, month):
        self._year = year
        self._month = month

    def build(self, cur_page_index=0) -> str:
        return self.base_template.format(
            year=str(self._year)[-2:],
            month=str(self._month).rjust(2, '0'),  # padding months: 1 -> '01', 11 -> '11',
            cur_page_index=cur_page_index*self.max_links_per_page,
            max_links_per_page=self.max_links_per_page
        )

def main() -> None:  # pragma: no cover
    """
    Entrypoint for scrapper module
    """
    CRAWLER_CONFIG_PATH = Path(__file__).parent / 'assets' / 'config.json'
    configuration = Config(CRAWLER_CONFIG_PATH)
    session = make_session(configuration)

    submissions = []
    for year in tqdm(range(1993, 2023+1)):
        if year == 1994:
            # TODO: remove once scales for 1 year
            break

        for month in tqdm(range(1, 12+1)):
            if month == 2:
                # TODO: remove once scales for 1 month
                break

            url = TargetURL(year, month).build()

            parser = HTMLParser(url, session)

            max_pages = parser.retrieve_max_pages()

            for page in tqdm(range(max_pages)):
                if page == 2:
                    # TODO: remove once scales for 1 page
                    break

                url = TargetURL(year, month).build(cur_page_index=page)
                parser = HTMLParser(url, session)
                submissions.extend(parser.collect_metadata())

    print(f'Collected {len(submissions)} submissions!')



if __name__ == '__main__':  # pragma: no cover
    main()
