import datetime
from urllib.parse import urlparse

from googlesearch import search
from tqdm import tqdm

from arxiv_scrapper.dto.submission_dto import (SubmissionDTO,
                                               SubmissionQueryResultDTO)
from arxiv_scrapper.dto.target_url import SearchFeedURL


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
