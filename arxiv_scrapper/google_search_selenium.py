import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def scroll_to_bottom(browser, times):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    # last_height = browser.execute_script("return document.body.scrollHeight")

    for _ in range(times):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # # Calculate new scroll height and compare with last scroll height
        # last_height = browser.execute_script("return document.body.scrollHeight")


def is_arxiv_link(url: str):
    parsed_url = urlparse(url)

    is_target = any(i in parsed_url.path for i in ('abs', 'pdf'))

    return parsed_url.netloc == 'arxiv.org' and is_target


def search(browser, title):
    search = browser.find_element(By.NAME, 'q')
    search.send_keys(f"{title} site:arxiv.org")
    search.send_keys(Keys.RETURN)  # hit return after you enter search text
    time.sleep(0.1)  # sleep for 5 seconds so you can see the results

    scroll_to_bottom(browser, 3)

    html = browser.page_source

    soup = BeautifulSoup(html, features='lxml')

    # links = soup.find(id='rso').find_all('div', recursive=False)

    # desired_class = links[1].get('class')[0]

    links = soup.find_all('a', {'jsname': True, 'data-ved': True})

    urls = []
    for link in links:
        # link = search_result.find('a')
        # if link is None:
        #     continue
        url = link.get("href")
        if url is None:
            continue
        urls.append(url)

    only_target_links = list(map(lambda x: x.replace('pdf', 'abs'), filter(is_arxiv_link, urls)))
    return only_target_links


def main():
    browser = webdriver.Chrome()
    browser.get('http://www.google.com')
    title = 'lora adapters fine-tuning'
    only_target_links = search(browser, title)
    print(len(only_target_links), only_target_links)

    browser.get('http://www.google.com')
    title = 'hebb learning computer vision'
    only_target_links = search(browser, title)
    print(len(only_target_links), only_target_links)

    browser.quit()


if __name__ == '__main__':
    main()
