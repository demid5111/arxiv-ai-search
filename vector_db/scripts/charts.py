import argparse
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


class Charts():
    def __init__(self, path: Union[str, Path]) -> None:
        self.month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.df = pd.read_csv(path)

    def all_years(self, save_path: Path = Path('./dist'), start_year: int = 1993, union_year: int = 2011, end_year: int = 2023):
        labels_pie = []
        values_pie = []
        sum_union_year = self.df[self.df._year <= union_year]._year.count()
        labels_pie.append(f'{start_year}-{union_year}')
        values_pie.append(sum_union_year)
        for i in range(union_year + 1, end_year + 1):
            sum_year = self.df[self.df._year == i]._year.count()
            labels_pie.append(str(i))
            values_pie.append(sum_year)
        plt.clf()
        fig, ax = plt.subplots()
        ax.pie(values_pie, labels=labels_pie)
        print(list(plt.cm.colors.cnames.keys()))
        plt.savefig(save_path / 'all_years.png')

    def current_years(self, save_path: Path = Path('./dist')):
        current_month = []

        for i in self.month_list:
            work_month = self.df[self.df._month == i]
            result = work_month._year.count()
            current_month.append(result)
        plt.clf()
        fig, ax = plt.subplots()
        ax.bar(self.month_list, current_month)
        fig.suptitle('fgf')
        ax.set_xlabel('Месяцы')
        ax.set_ylabel('Количество')
        plt.savefig(save_path / f'figure_bar.png')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path)
    return parser.parse_args()


def main():
    args = get_args()
    charts = Charts(Path(args.path))

    charts.all_years()
    charts.current_years()


if __name__ == '__main__':
    main()
