import datetime
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

import googlesearch
import requests
from bs4 import BeautifulSoup
from googlesearch import SearchResult

from arxiv_scrapper.connection import Config, make_session
from arxiv_scrapper.dto.submission_dto import (SubmissionDTO,
                                               SubmissionQueryResultDTO)
from arxiv_scrapper.dto.target_url import SearchFeedURL


def _req(term, results, lang, start, proxies, timeout):
    print('Patched request function for googlesearch library')
    requests.packages.urllib3.disable_warnings() 
    CRAWLER_CONFIG_PATH = Path(__file__).parent / 'assets' / 'config.json'
    configuration = Config(CRAWLER_CONFIG_PATH)
    session = make_session(configuration)

    resp = session.get(
        url="https://www.google.com/search",
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp



def search(term, num_results=10, lang="en", advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = term.replace(" ", "+")

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        print('request...', flush=True)
        resp = _req(escaped_term, num_results - start,
                    lang, start, timeout)
        print('now parse...', flush=True)
        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        print('sleep...')
        sleep(sleep_interval)

googlesearch._req = _req
googlesearch.search = search

class SearchFeedParser:
    @staticmethod
    def run(row, top_n=5) -> SubmissionQueryResultDTO:
        submission = SubmissionDTO(*row)

        # query_results = list('fake' for _ in range(10))
        # return SubmissionQueryResultDTO(submission, query_results[:top_n])

        url = SearchFeedURL(submission._title).url
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {url}', flush=True)

        # 5 * 12 = 60 seconds per 1 page
        # 300 seconds per 5 articles (one month)
        # 3600 seconds per 1 year
        # 5 hours per whole run
        res = search(
            submission._title + ' site:arxiv.org',
            sleep_interval=20,
            num_results=10,  # itself + 1 (for chance) + 10 arxiv links
            advanced=True
        )
        print('before loop')
        query_results = []
        for i in res:
            parsed_url = urlparse(i.url)
            is_same_paper = parsed_url.path.split('/')[-1] == submission._url.split('/')[-1]
            if parsed_url.netloc != 'arxiv.org' or 'pdf' not in parsed_url.path or is_same_paper:
                continue
            print(f'Appending {i.url}')
            query_results.append(parsed_url.path.replace('pdf', 'abs'))

        if len(query_results) < top_n:
            print(f'For {submission._url} did not get {top_n} recommendations!')

        print('Finished with parsing')
        return SubmissionQueryResultDTO(submission, query_results[:top_n])
