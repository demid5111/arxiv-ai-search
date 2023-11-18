from itertools import product
from pathlib import Path
import multiprocessing as mp

import requests
import pandas as pd

from arxiv_scrapper.config_dto import Config
from arxiv_scrapper.connection import make_session
from arxiv_scrapper.constants import DIST_PATH
from arxiv_scrapper.parser import SingleMonthParser


def process_single_month(year, month, session):
    dump_path = DIST_PATH / f'{year}_{month}.csv'
    if dump_path.exists():
        print(f'Skipping {year=} {month=} ...')
        return

    print(f'Processing {year=} {month=}')
    parser = SingleMonthParser(session, year, month)
    month_submissions = parser.run()

    if not month_submissions:
        print(f'No submissions back in {year=} {month=}')

    raw = [submission.__dict__ for submission in month_submissions]
    df = pd.DataFrame(raw)
    df.to_csv(dump_path)


def main() -> None:  # pragma: no cover
    """
    Entrypoint for scrapper module
    """
    requests.packages.urllib3.disable_warnings()

    CRAWLER_CONFIG_PATH = Path(__file__).parent / 'assets' / 'config.json'
    configuration = Config(CRAWLER_CONFIG_PATH)
    session = make_session(configuration)

    years = range(1993, 2023 + 1)
    months = range(1, 12 + 1)
    combinations = list(product(years, months))

    pool = mp.Pool(mp.cpu_count())

    result_objects = (
        pool.apply_async(process_single_month, args=(year, month, session))
        for year, month in combinations
    )

    results = (r.get() for r in result_objects)

    print(len(list(results)))


if __name__ == '__main__':  # pragma: no cover
    main()
