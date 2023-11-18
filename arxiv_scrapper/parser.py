import datetime
import re

from bs4 import BeautifulSoup


class Submission:
    def __init__(self, url, year, month):
        self._url = url
        self._year = year
        self._month = month

class HTMLParser:
    def __init__(self, full_url: str, session) -> None:
        """
        Initializes an instance of the HTMLParser class
        """

        self._article_url = full_url
        self._session = session

    def retrieve_max_pages(self):
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {self._article_url}', flush=True)

        feed_request = self._session.get(self._article_url)

        feed_soup = BeautifulSoup(feed_request.text, features='lxml')

        page_title_bs = feed_soup.find('h2')
        pages_links_bs = page_title_bs.find_next_sibling('small')

        return len(pages_links_bs.find_all('a')) + 1  # current page should count, but it is active - no link for it

    def collect_metadata(self):
        print(f'{datetime.datetime.now()} (HTMLParser.retrieve_max_pages) Accessing {self._article_url}', flush=True)

        feed_request = self._session.get(self._article_url)

        feed_soup = BeautifulSoup(feed_request.text, features='lxml')

        month, year = feed_soup.find('h2').text.split()[-2:]

        submission_descriptors_bs = feed_soup.find_all('dt')
        submissions = []
        for submission_bs in submission_descriptors_bs:
            url = submission_bs.find('span').find('a', title='Abstract').get('href')
            submissions.append(Submission(url, year, month))

        return submissions




    def parse(self):
        """
        Parses each article
        """
        print(f'{datetime.datetime.now()} (ArticleParser.parse) Accessing {self.article_url}',
              flush=True)

        article_request = make_request(self.article_url, self._config)

        if not article_request.ok:  # pragma: no cover
            print(f'Error: {article_request.status_code}', flush=True)
            return article_request.ok
        print(f'{datetime.datetime.now()} (ArticleParser.parse) '
              f'obtained result for {self.article_url}',
              flush=True)
        time.sleep(2)
        print(f'{datetime.datetime.now()} (ArticleParser.parse) '
              f'2 seconds are over {self.article_url}',
              flush=True)

        article_soup = BeautifulSoup(article_request.text, features='lxml')

        self._fill_article_with_text(article_soup)
        self._fill_article_with_meta_information(article_soup)

        return self.article

    def _fill_article_with_text(self, article_soup: BeautifulSoup) -> None:
        """
        Finds text of article
        """
        texts = article_soup.find_all('p')
        res_text = ''
        for text in texts:
            res_text += text.text + '\n'
        self.article.text = res_text

    def _fill_article_with_meta_information(self, article_soup: BeautifulSoup) -> None:
        """
        Finds meta information of article
        """
        self.article.title = article_soup.find("h1").text

        try:
            raw_date = article_soup.find('time').get('datetime').replace('T', ' ')
            self.article.date = self.unify_date_format(raw_date)
        except AttributeError:  # pragma: no cover
            self.article.date = self.unify_date_format('2022-01-01 01:01:01')

        try:
            author_soup = article_soup.find_all("div", itemprop="author")[0]
            authors = author_soup.find_all("p", itemprop="name")[0].text.split(',')
            for author in authors:
                self.article.author.append(author.strip())
        except (AttributeError, IndexError):  # pragma: no cover
            self.article.author = ["NOT FOUND"]
            print(f"No author for article {self.article.article_id} found")
        try:
            self.article.topics.append(
                article_soup.find("li", itemprop="itemListElement").find("span").text)
        except AttributeError:  # pragma: no cover
            print(f"No topics for article {self.article.article_id} found")

    def unify_date_format(self, date_str: str) -> datetime.datetime:
        """
        Unifies date format
        """
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
