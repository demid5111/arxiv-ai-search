import multiprocessing as mp
from itertools import product
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

from arxiv_scrapper.connection import make_session
from arxiv_scrapper.constants import DIST_PATH
from arxiv_scrapper.dto.config_dto import Config
from arxiv_scrapper.dto.submission_dto import NUM_TO_MONTH
from arxiv_scrapper.search_feed_parser import SearchFeedParser
from arxiv_scrapper.single_article_parser import SingleArticleParser


def load_submissions(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, engine='pyarrow')

    df['_year'] = df['_year'].astype('int')

    df.reset_index(inplace=True, drop=True)

    df.drop([''], axis=1, inplace=True)

    return df


def process_single_month(year, month, session, submissions_df) -> None:
    print(f'Processing {year=} {month=}')

    artifacts_path = DIST_PATH / 'tmp_val'
    artifacts_path.mkdir(exist_ok=True)
    dump_path = artifacts_path / f'val_{year}_{month}.csv'

    if dump_path.exists():
        print(f'Skipping {year=} {month=} ...')
        return

    parser = SearchFeedParser(session, year, month)

    submissions = submissions_df[
        (submissions_df['_year'] == year) &
        (submissions_df['_month'] == NUM_TO_MONTH[month])
        ].values
    submissions = submissions[:10]

    query_results = [parser.run(row) for row in submissions]

    # pool = mp.Pool(mp.cpu_count())
    #
    # result_objects = (pool.apply_async(parser.run, args=(row, )) for row in submissions)
    #
    # results = (r.get() for r in result_objects)

    raw = [submission.as_dict() for submission in query_results]
    df = pd.DataFrame(raw)
    df.to_csv(dump_path)


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    requests.packages.urllib3.disable_warnings()

    crawler_config_path = Path(__file__).parent / 'assets' / 'config.json'
    arxiv_index_path = Path(__file__).parent / 'dist' / 'tmp_abstract' / 'abs_2021_2.csv'

    configuration = Config(crawler_config_path)
    session = make_session(configuration)

    years = range(1993, 2023 + 1)
    months = range(1, 12 + 1)
    combinations = list(product(years, months))
    submissions_df = load_submissions(arxiv_index_path)

    # for _, (year, month) in tqdm(enumerate(combinations)):
    process_single_month(2021, 2, session, submissions_df)


if __name__ == '__main__':
    main()
