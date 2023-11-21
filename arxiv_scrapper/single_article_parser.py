import datetime
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

from arxiv_scrapper.dto.submission_dto import SubmissionDTO
from arxiv_scrapper.dto.target_url import ArticleURL


class SingleArticleParser:
    def __init__(self, session, year, month):
        self._session = session
        self._year = year
        self._month = month
        self._date_pattern = re.compile(
            r'Authors and titles for (?P<month>\w+)\s+(?P<year>\d+).*')

    def run(self, submission):
        return self._collect_single_page_metadata(submission)

    def _collect_single_page_metadata(self, row: tuple):
        submission = SubmissionDTO(*row[1:])
        url = ArticleURL(submission._url).url
        print(
            f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {url}', flush=True)

        # feed_request = self._session.get(ArticleURL(submission._url).url)
        # content = feed_request.text
        with open(r'C:\Users\a00815200\Downloads\[2305.14314] QLoRA_ Efficient Finetuning of Quantized LLMs.html', encoding='utf-8') as f:
            content = f.read()

        feed_soup = BeautifulSoup(content, features='lxml')

        submission.set_title(feed_soup.find(id='abs').find('h1').text)

        submission.set_submit_date(
            feed_soup.find('div', {'class': 'dateline'}).text)

        authors_bs = feed_soup.find(id='abs').find(
            'div', {'class': 'authors'}).find_all('a')
        authors = list(
            map(
                lambda tag_bs: tag_bs.text.strip(),
                authors_bs
            )
        )
        submission.set_authors(','.join(authors))

        submission.set_abstract(feed_soup.find(
            id='abs').find('blockquote').text.strip())

        return submission
