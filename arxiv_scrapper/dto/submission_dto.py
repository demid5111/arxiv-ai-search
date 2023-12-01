import datetime

month_to_num = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}
NUM_TO_MONTH = {num: month.capitalize() for month, num in month_to_num.items()}


class SubmissionDTO:
    def __init__(self, url, year, month, title=None, abstract=None, submit_date=None, authors=None):
        self._url = url
        self._year = year
        self._month = month
        self._title = title
        self._abstract = abstract
        self._submit_date = submit_date
        self._authors = authors

    def set_title(self, title):
        self._title = title

    def set_abstract(self, abstract):
        self._abstract = abstract

    def set_submit_date(self, date_str: str):
        raw = date_str.strip().lower().removeprefix('[submitted on ')
        day, month, year = raw[:raw.index(']')].split()[:3]

        month = month_to_num[month]

        self._submit_date = datetime.datetime(
            day=int(day), month=month, year=int(year)).strftime('%d/%m/%Y')

    def set_authors(self, authors):
        self._authors = authors


class SubmissionQueryResultDTO:
    def __init__(self, submission, query_results):
        self._submission = submission
        self._query_results = query_results

    def as_dict(self):
        return {
            'query_article_link': self._submission._url,
            **{f'top_{i+1}': link for i, link in enumerate(self._query_results)}
        }
