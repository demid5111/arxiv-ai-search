import time
from urllib.parse import urlencode, urlparse

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scroll_to_bottom(browser, times) -> None:
    scroll_pause_time = 5

    for _ in range(times):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)


def is_arxiv_link(url: str):
    parsed_url = urlparse(url)
    is_target = any(i in parsed_url.path for i in ('abs', 'pdf'))
    return parsed_url.netloc == 'arxiv.org' and is_target


def search(browser, title):
    new_url = 'https://www.google.com/search?' + urlencode({'q': f"{title} site:arxiv.org"})
    browser.get(new_url)

    # search_field = browser.find_element(By.NAME, 'q')
    # search_field.send_keys(f"{title} site:arxiv.org")
    # search_field.send_keys(Keys.RETURN)  # hit return after you enter search text
    time.sleep(15)  # sleep for 5 seconds so you can see the results

    scroll_to_bottom(browser, 1)

    html = browser.page_source

    soup = BeautifulSoup(html, features='lxml')

    links = soup.find_all('a', {'jsname': True, 'data-ved': True})

    urls = [link.get("href") for link in links if link.get("href") ]

    return list(
        map(
            lambda x: urlparse(x).path.replace('pdf', 'abs'),
            filter(is_arxiv_link, urls)
        )
    )
