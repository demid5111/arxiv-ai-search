from pathlib import Path

import pandas as pd


class SubmissionDTO:
    def __init__(self, url, year, month):
        self._url = url
        self._year = year
        self._month = month


def load_submissions(path: Path) -> list[SubmissionDTO]:
    df = pd.read_csv(path)

    df['_year'] = df['_year'].astype('int')

    # joint_df.reset_index(inplace=True, drop=True)

    return df.apply(SubmissionDTO, axis=1).tolist()
