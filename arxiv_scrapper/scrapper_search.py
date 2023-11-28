from itertools import product
from pathlib import Path

import pandas as pd
import pyarrow as pa
import requests
from pyarrow import csv
from tqdm import tqdm

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


def process_single_month(year, month, submissions_df) -> None:
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
    submissions = submissions[:3]

    query_results = [SearchFeedParser.run(row) for row in submissions]

    print('Finished with queries')

    raw = [submission.as_dict() for submission in query_results]
    df = pd.DataFrame(raw)
    df.to_csv(dump_path)
    print('Finished with dump')


def main() -> None:
    """
    Entrypoint for scrapper module
    """
    requests.packages.urllib3.disable_warnings()

    arxiv_index_path = Path(__file__).parent / 'assets' / 'arxiv_abs_Nov_2023.csv'

    years = range(2018, 2023 + 1)
    months = range(1, 12 + 1)
    combinations = list(product(years, months))
    submissions_df = load_submissions(arxiv_index_path)

    import sys
    _, year, month = sys.argv
    print(f'{year=} {month=}')

    process_single_month(int(year), int(month), submissions_df)

    # for _, (year, month) in tqdm(enumerate(combinations), total=len(combinations)):
    #     process_single_month(year, month, submissions_df)


if __name__ == '__main__':
    main()
