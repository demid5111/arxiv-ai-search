from pathlib import Path

import pandas as pd

from arxiv_scrapper.constants import DIST_PATH


def _process(path_to_compress: Path, has_year: bool = True):
    joint_df = pd.concat(
        map(
            pd.read_csv,
            filter(
                lambda x: x.name != 'arxiv_final.csv',
                path_to_compress.glob('*.csv')
            )
        ),
        ignore_index=True,
        sort=False
    )
    joint_df = joint_df.drop('Unnamed: 0', axis=1)

    if has_year:
        joint_df['_year'] = joint_df['_year'].astype('int')

    joint_df.reset_index(inplace=True, drop=True)

    print(f'The greatest arXiv has {len(joint_df)} papers for Computer Science!')

    joint_df.to_csv(path_to_compress / 'arxiv_final.csv')


def main():
    path_to_compress = DIST_PATH / 'tmp_index'
    path_to_compress = DIST_PATH / 'tmp_abstract'
    path_to_compress = DIST_PATH / 'tmp_val'
    _process(path_to_compress, has_year=False)


if __name__ == '__main__':
    main()
