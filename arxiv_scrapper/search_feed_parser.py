from arxiv_scrapper.dto.submission_dto import (SubmissionDTO,
                                               SubmissionQueryResultDTO)
from arxiv_scrapper.google_search_selenium import search


class SearchFeedParser:
    @staticmethod
    def run(row, browser, top_n=10) -> SubmissionQueryResultDTO:
        submission = SubmissionDTO(*row)

        browser.get('http://www.google.com')

        only_target_links = search(browser, submission._title)

        print(len(only_target_links), flush=True)

        without_myself = list(filter(lambda x: x != submission._url, only_target_links))

        return SubmissionQueryResultDTO(submission, without_myself[:top_n])
