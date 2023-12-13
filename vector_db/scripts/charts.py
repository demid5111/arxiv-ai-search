import argparse
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Charts():
    def __init__(self, path: Union[str, Path]) -> None:
        self.month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.df = pd.read_csv(path)

    def all_years(self, save_path: Path = Path('./dist'), start_year: int = 1993, union_year: int = 2011, end_year: int = 2023):
        labels = []
        values = []
        sum_union_year = self.df[self.df._year <= union_year]._year.count()
        labels.append(f'{start_year}-{union_year}')
        values.append(sum_union_year)
        for i in range(union_year + 1, end_year + 1):
            sum_year = self.df[self.df._year == i]._year.count()
            labels.append(str(i))
            values.append(sum_year)
        index = 'Year'
        y_offset = np.zeros(1)
        _, ax = plt.subplots()
        cmap = plt.colormaps['tab20']
        outer_colors = cmap(np.arange(13))
        for row in range(len(values)):
            ax.bar(index, values[row], label=labels[row], width=0.7,
                   bottom=y_offset, color=outer_colors[row])
            y_offset = y_offset + values[row]
        ax.legend(loc="upper right")
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlim(-2, 2)
        plt.savefig(save_path / 'articles_in_every_year.png')

    def articles_by_months(self, save_path: Path = Path('./dist')):
        current_month = []

        for i in self.month_list:
            work_month = self.df[self.df._month == i]
            result = work_month._year.count()
            current_month.append(result)
        plt.clf()
        _, ax = plt.subplots()
        ax.bar(self.month_list, current_month)
        ax.set_xlabel('Months')
        ax.set_ylabel('Count')
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='both', linestyle='--', linewidth=0.5, color='0.7')
        ax.set_axisbelow(True)
        plt.savefig(save_path / 'number_of_articles_by_month.png')

    def articles_in_years(self, start_year: int = 1993, end_year: int = 2023, save_path: Path = Path('./dist')):
        labels_plot = []
        values_plot = []
        for i in range(start_year, end_year + 1):
            sum_year = self.df[self.df._year == i]._year.count()
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
        plt.savefig(save_path / 'number_of_articles_in_years.png')


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
