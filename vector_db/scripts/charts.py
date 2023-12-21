import argparse
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Charts():
    def __init__(self, path: Union[str, Path]) -> None:
        self.month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.dpi = 600
        self.df = pd.read_csv(path)

    def all_years(self, save_path: Path = Path('./dist'), start_year: int = 1993, union_year: int = 2011, end_year: int = 2023):
        tab20b_cm = [plt.colormaps['tab20b'](v)
                     for v in np.linspace(0.05, 0.9, 8)]
        tab20c_cm = [plt.colormaps['tab20c'](v)
                     for v in np.linspace(0.05, 0.45, 5)]
        outer_colors = tab20b_cm + tab20c_cm
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
        _, ax = plt.subplots()
        ax.pie(values_pie, labels=labels_pie, wedgeprops={
               'linewidth': 0.5, "edgecolor": 'white'}, colors=outer_colors)
        plt.savefig(save_path / 'articles_in_every_year.pdf', dpi=self.dpi)
        plt.close()

    def articles_by_months(self, save_path: Path = Path('./dist')):
        tab20b_cm = [plt.colormaps['tab20b'](v)
                     for v in np.linspace(0.05, 0.9, 8)]
        tab20c_cm = [plt.colormaps['tab20c'](v)
                     for v in np.linspace(0.05, 0.4, 4)]
        outer_colors = tab20b_cm + tab20c_cm
        # outer_colors = plt.colormaps['tab20b'](0.25)
        current_month = []

        for i in self.month_list:
            work_month = self.df[self.df._month == i]
            result = work_month._year.count()
            current_month.append(result)
        plt.clf()
        _, ax = plt.subplots()
        ax.bar(self.month_list, current_month, color=outer_colors)
        ax.set_xlabel('Months')
        ax.set_ylabel('Count')
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='both', linestyle='--', linewidth=0.5, color='0.7')
        ax.set_axisbelow(True)
        plt.savefig(save_path / 'number_of_articles_by_month.pdf', dpi=self.dpi)
        plt.close()

    def articles_in_years(self, start_year: int = 1993, end_year: int = 2023, save_path: Path = Path('./dist')):
        labels_plot = []
        values_plot = []
        sum_year = 0
        for i in range(start_year, end_year + 1):
            sum_year += self.df[self.df._year == i]._year.count()
            labels_plot.append(int(i))
            values_plot.append(sum_year)
        plt.clf()
        _, ax = plt.subplots(figsize=(8, 6))
        ax.plot(labels_plot, values_plot)
        ax.set_xlabel('Years')
        ax.set_ylabel('Count')
        start, end = min(labels_plot), max(labels_plot)
        ax.xaxis.set_ticks(np.arange(start, end + 1, 2))
        ax.xaxis.set_tick_params(rotation=45, labelsize=8)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='both', linestyle='--', linewidth=0.5, color='0.7')
        plt.savefig(save_path / 'number_of_articles_in_years.pdf', dpi=self.dpi)
        plt.close()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=Path)
    return parser.parse_args()


def main():
    args = get_args()
    charts = Charts(Path(args.path))

    charts.all_years()
    charts.articles_by_months()
    charts.articles_in_years()


if __name__ == '__main__':
    main()
