import math
import os
import sys
from typing import Dict

import matplotlib
import matplotlib.pyplot
import numpy
import pandas
from gym.envs.registration import patch_deprecated_methods


def invalid_moves_while_learning(folder):
    headers = ['invalid', 'reward', 'cards_played']
    data: Dict[str, numpy.ndarray] = {}
    files = ("0defence", "10defence", "29defence")

    for data_file in sorted(sorted(os.listdir(folder)), key=len):
        for f in files:
            if data_file.startswith(f):
                df = pandas.read_csv(os.path.join(folder, data_file), names=headers)
                data[f] = df['invalid']

    x = numpy.arange(len(data[f]))

    fig, ax = matplotlib.pyplot.subplots()
    for key, values in data.items():
        ax.plot(x, values, label=key)

    ax.set_title('Invalid moves while learning rules')
    ax.set_ylabel('Invalid moves')
    ax.set_xlabel('Epochs')
    ax.legend()
    fig.tight_layout()


def validation_tricks_won(folders):
    return _draw_boxchart(folders, 'tricks_won', 'Mean tricks won on validation', 'Mean tricks')


def validation_invalid(folders):
    return _draw_boxchart(folders, 'invalid', 'Invalid moves on validation', 'Invalid moves')


def _draw_boxchart(folders, column, title, y_label):
    headers = ['invalid', 'tricks_won', 'cards_played']
    data: Dict[str, numpy.ndarray] = {}
    fig, ax = matplotlib.pyplot.subplots()
    labels = ['initial state', 'learning rules', 'learning both rules and q value']
    colors = ['green', 'blue', 'aqua']
    legend = []

    for i, folder in enumerate(folders):
        width = 1 / (len(os.listdir(folder)) + 1)
        for data_file in sorted(sorted(os.listdir(folder)), key=len):
            dataset = " ".join(data_file.split('.')[0])
            df = pandas.read_csv(os.path.join(folder, data_file), names=headers)
            data[dataset] = df[column]

        x = numpy.arange(len(data.items()))
        x = x - width + (i * width)
        box = ax.boxplot(data.values(), widths=width, positions=x, patch_artist=True)
        for patch in box['boxes']:
            patch.set_facecolor(colors[i])
        legend.append(patch)

    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xticks(numpy.arange(len(data.keys())))
    ax.set_xticklabels(data.keys())
    ax.set_yticks(range(math.ceil(ax.get_ylim()[1])))
    ax.legend(legend, labels)
    fig.tight_layout()

    matplotlib.pyplot.grid(True, 'both', 'y', alpha=0.8)


if __name__ == "__main__":
    _, *folders = sys.argv
    data = {"offence": [], "defence": []}
    invalid_moves_while_learning(folders[1].split('/')[0])
    validation_invalid(folders)
    validation_tricks_won(folders)
    matplotlib.pyplot.show()
