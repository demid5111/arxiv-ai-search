import datetime
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

from arxiv_scrapper.dto.submission_dto import SubmissionDTO


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
            cur_page_index=cur_page_index * self.max_links_per_page,
            max_links_per_page=self.max_links_per_page
        )


class SingleMonthParser:
    def __init__(self, session, year, month):
        self._session = session
        self._year = year
        self._month = month
        self._date_pattern = re.compile(r'Authors and titles for (?P<month>\w+)\s+(?P<year>\d+).*')

    def run(self):
        url = TargetURL(self._year, self._month).build()
        max_pages = self._retrieve_max_pages(url)

        submissions = []
        for page in tqdm(range(max_pages)):
            url = TargetURL(self._year, self._month).build(cur_page_index=page)
            submissions.extend(self._collect_single_page_metadata(url))

        return submissions

    def _retrieve_max_pages(self, url):
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {url}', flush=True)

        feed_request = self._session.get(url)

        feed_soup = BeautifulSoup(feed_request.text, features='lxml')

        page_title_bs = feed_soup.find('h2')
        pages_links_bs = page_title_bs.find_next_sibling('small')

        if not pages_links_bs:
            # for ancient years, like 1993 there could be months with no submissions at all!
            return 0

        return len(pages_links_bs.find_all('a')) + 1  # current page should count, but it is active - no link for it

    def _collect_single_page_metadata(self, url):
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {url}', flush=True)

        feed_request = self._session.get(url)

        feed_soup = BeautifulSoup(feed_request.text, features='lxml')

        res_match = re.match(self._date_pattern, feed_soup.find('h2').text)

        month = res_match.group('month')
        year = res_match.group('year')

        submission_descriptors_bs = feed_soup.find_all('dt')
        submissions = []
        for submission_bs in submission_descriptors_bs:
            if 'error with ' in submission_bs.text.lower():
                print(submission_bs.text, 'skip...')
                continue
            url = submission_bs.find('span').find('a', title='Abstract').get('href')
            submissions.append(SubmissionDTO(url, int(year), month))

        return submissions
