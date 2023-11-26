import datetime

from bs4 import BeautifulSoup

from arxiv_scrapper.dto.submission_dto import SubmissionDTO, SubmissionQueryResultDTO
from arxiv_scrapper.dto.target_url import SearchFeedURL


class SearchFeedParser:
    def __init__(self, session, year, month):
        self._session = session
        self._year = year
        self._month = month

    def run(self, row) -> SubmissionQueryResultDTO:
        submission = SubmissionDTO(*row)
        url = SearchFeedURL(submission._title).url
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {url}', flush=True)

        content = self._session.get(url).text

        feed_soup = BeautifulSoup(content, features='lxml')

        query_results = [
            item.find('p', {'class': 'list-title'}).find('a').get('href').removeprefix('https://arxiv.org/')
            for item in feed_soup.find_all('li', {'class': 'arxiv-result'})
        ]

        return SubmissionQueryResultDTO(submission, query_results)
