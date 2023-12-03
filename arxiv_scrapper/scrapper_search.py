import time
from itertools import product
from pathlib import Path

import pandas as pd
import pyarrow as pa
import requests
from pyarrow import csv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.firefox.service import Service as FirefoxService
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from arxiv_scrapper.constants import DIST_PATH
from arxiv_scrapper.dto.submission_dto import NUM_TO_MONTH
from arxiv_scrapper.search_feed_parser import SearchFeedParser


def load_submissions(path: Path) -> pd.DataFrame:
    pa_table = pa.csv.read_csv(path, read_options=pa.csv.ReadOptions(block_size=1e9))
    df = pa_table.to_pandas()
    df['_year'] = df['_year'].astype('int')
    df.reset_index(inplace=True, drop=True)
    df.drop([''], axis=1, inplace=True)
    return df


def process_single_month(year, month, submissions_df, browser) -> None:
    print(f'Processing {year=} {month=}')

    artifacts_path = DIST_PATH / 'tmp_val'
    artifacts_path.mkdir(exist_ok=True)
    dump_path = artifacts_path / f'val_{year}_{month}.csv'

    if dump_path.exists():
        print(f'Skipping {year=} {month=} ...')
        return

    submissions = submissions_df[
        (submissions_df['_year'] == year) &
        (submissions_df['_month'] == NUM_TO_MONTH[month])
        ].values
    submissions = submissions[:10]

    query_results = [
        SearchFeedParser.run(row, browser) 
        for row in tqdm(submissions, total=len(submissions))
    ]

    raw = [submission.as_dict() for submission in query_results]
    df = pd.DataFrame(raw)
    df.to_csv(dump_path)


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    requests.packages.urllib3.disable_warnings()

    arxiv_index_path = Path(__file__).parent / 'assets' / 'arxiv_abs_Nov_2023.csv'

    years = range(2019, 2023 + 1)
    months = range(9, 12 + 1)
    combinations = list(product(years, months))
    submissions_df = load_submissions(arxiv_index_path)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"--window-size=1920,1080")
    options.add_argument("--hide-scrollbars")
    
    for i, (year, month) in tqdm(enumerate(combinations), total=len(combinations)):
        service = ChromiumService(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)

        # print(GeckoDriverManager().install())
        # service = FirefoxService(
        #     executable_path=GeckoDriverManager().install(),
        #     firefox_binary='/usr/bin/firefox'
        # )
        # browser = webdriver.Firefox(service=service, options=options)
        browser.get('http://www.google.com')
        delay = 30 # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, 'q')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        
        process_single_month(year, month, submissions_df, browser)

        page_path_root = Path(__file__).parent  / f'dist' / 'screens' 
        page_path_root.mkdir(exist_ok=True)
        # page_path = page_path_root / f'{i}.html'
        # with page_path.open('w', encoding='utf-8') as f:
        #     f.write(browser.page_source)
        # browser.save_screenshot(f'{i}.png')
        browser.quit()

        time.sleep(15)


if __name__ == '__main__':
    main()
