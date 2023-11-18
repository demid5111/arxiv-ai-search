from functools import partial

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from arxiv_scrapper.config_dto import Config


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
