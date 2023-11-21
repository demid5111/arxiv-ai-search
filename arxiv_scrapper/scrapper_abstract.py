from itertools import product
from pathlib import Path
import multiprocessing as mp

import pandas as pd
import requests
from tqdm import tqdm

from arxiv_scrapper.dto.config_dto import Config
from arxiv_scrapper.connection import make_session
from arxiv_scrapper.constants import DIST_PATH
from arxiv_scrapper.dto.submission_dto import SubmissionDTO, NUM_TO_MONTH
from arxiv_scrapper.single_article_parser import SingleArticleParser


def load_submissions(path: Path) -> list[SubmissionDTO]:
    df = pd.read_csv(path, engine='pyarrow')

    df['_year'] = df['_year'].astype('int')

    df.reset_index(inplace=True, drop=True)

    return df


def process_single_month(year, month, session, submissions_df):
    print(f'Processing {year=} {month=}')

    artifacts_path = DIST_PATH / 'tmp_abstract'
    artifacts_path.mkdir(exist_ok=True)
    dump_path = artifacts_path / f'{year}_{month}.csv'
    if dump_path.exists():
        print(f'Skipping {year=} {month=} ...')
        return

    parser = SingleArticleParser(session, year, month)

    submissions = submissions_df[
        (submissions_df['_year'] == year) &
        (submissions_df['_month'] == NUM_TO_MONTH[month])
    ].values

    new_submissions = [parser.run(row) for row in submissions]

    if not new_submissions:
        print(f'No submissions back in {year=} {month=}')

    raw = [submission.__dict__ for submission in new_submissions]
    df = pd.DataFrame(raw)
    df.to_csv(dump_path)


def main() -> None:  # pragma: no cover
    """
    Entrypoint for scrapper module
    """
    requests.packages.urllib3.disable_warnings()

    CRAWLER_CONFIG_PATH = Path(__file__).parent / 'assets' / 'config.json'
    ARXIV_INDEX_PATH = Path(__file__).parent / \
        'assets' / 'arxiv_index_Nov_2023.csv'
    configuration = Config(CRAWLER_CONFIG_PATH)
    session = make_session(configuration)

    years = range(1993, 2023 + 1)
    months = range(1, 12 + 1)
    combinations = list(product(years, months))
    submissions_df = load_submissions(ARXIV_INDEX_PATH)

    # for i, (year, month) in tqdm(enumerate(combinations)):
    #     process_single_month(year, month, session, submissions_df)

    pool = mp.Pool(mp.cpu_count())

    result_objects = (
        pool.apply_async(process_single_month, args=(
            year, month, session, submissions_df))
        for year, month in combinations
    )

    results = (r.get() for r in result_objects)

    print(len(list(results)))


if __name__ == '__main__':
    main()
