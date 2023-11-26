import pandas as pd

from arxiv_scrapper.constants import DIST_PATH


def main():
    joint_df = pd.concat(
        map(
            pd.read_csv,
            filter(
                lambda x: x.name != 'arxiv_index_final.csv',
                (DIST_PATH / 'tmp_index').glob('*.csv')
            )
        ),
        ignore_index=True,
        sort=False
    )
    joint_df = joint_df.drop('Unnamed: 0', axis=1)

    joint_df['_year'] = joint_df['_year'].astype('int')

    joint_df.reset_index(inplace=True, drop=True)

    print(f'The greatest arXiv has {len(joint_df)} papers for Computer Science!')

    joint_df.to_csv(DIST_PATH / 'arxiv_index_final.csv')


if __name__ == '__main__':
    main()
