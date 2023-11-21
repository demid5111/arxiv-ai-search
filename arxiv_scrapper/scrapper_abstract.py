from itertools import product
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

from arxiv_scrapper.dto.config_dto import Config
from arxiv_scrapper.connection import make_session
from arxiv_scrapper.constants import DIST_PATH
from arxiv_scrapper.dto.submission_dto import load_submissions


def process_single_month(year, month, session):
    print(f'Processing {year=} {month=}')

    artifacts_path = DIST_PATH / 'tmp_abstract'
    artifacts_path.mkdir(exist_ok=True)
    dump_path = artifacts_path / f'{year}_{month}.csv'
    if dump_path.exists():
        print(f'Skipping {year=} {month=} ...')
        return

    parser = SingleArticleParser(session, year, month)

    new_submissions = [parser.run(submission) for submission in submissions]

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
    ARXIV_INDEX_PATH = DIST_PATH / 'assets' / 'arxiv_index_Nov_2023.csv'
    configuration = Config(CRAWLER_CONFIG_PATH)
    session = make_session(configuration)

    years = range(1993, 2023 + 1)
    months = range(1, 12 + 1)
    combinations = list(product(years, months))
    submissions = load_submissions(ARXIV_INDEX_PATH)

    for i, (year, month) in tqdm(enumerate(combinations)):
        if i == 1:
            break
        process_single_month(year, month, session)

    # pool = mp.Pool(mp.cpu_count())
    #
    # result_objects = (
    #     pool.apply_async(process_single_month, args=(year, month, session))
    #     for year, month in combinations
    # )
    #
    # results = (r.get() for r in result_objects)
    #
    # print(len(list(results)))


if __name__ == '__main__':  # pragma: no cover
    main()
