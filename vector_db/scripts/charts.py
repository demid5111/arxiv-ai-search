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
        palitra_pie = ['#445577', '#606d8a', '#7c859e', '#989fb2', '#b5bac7', '#d3d5db',
                       '#f1f1f1', '#f1d4d4', '#f0b8b8', '#ec9c9d', '#e67f83', '#de6069', '#de425b']
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
        ax.pie(values_pie, labels=labels_pie, wedgeprops={
               'linewidth': 1, "edgecolor": 'white'}, colors=palitra_pie)
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
        ax.set_xlabel('Months')
        ax.set_ylabel('Count')
        plt.savefig(save_path / f'figure_bar.png')

    def progression_graph(self, start_year: int = 1993, end_year: int = 2023, save_path: Path = Path('./dist')):
        labels_plot = []
        values_plot = []
        for i in range(start_year, end_year + 1):
            sum_year = self.df[self.df._year == i]._year.count()
            labels_plot.append(int(i))
            values_plot.append(sum_year)
        plt.clf()
        fig, ax = plt.subplots()
        ax.plot(labels_plot, values_plot)
        ax.set_xlabel('Years')
        ax.set_ylabel('Count')
        plt.savefig(save_path / f'progression_bar.png')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path)
    return parser.parse_args()


def main():
    args = get_args()
    charts = Charts(Path(args.path))

    charts.all_years()
    charts.current_years()
    charts.progression_graph()


if __name__ == '__main__':
    main()
