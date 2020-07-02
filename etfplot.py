#!/usr/bin/env python3

import re
import sys
import datetime
import mplcursors
import matplotlib.pyplot as pl
from matplotlib.ticker import AutoMinorLocator


def main():
    filepath = sys.argv[1]
    date_re = r'###\s(.*)'
    data_re = r'([A-Z0-9]+)\s+(.*?)\s+EUR\s([\d,]+)'
    try:
        filecontent = [line.strip() for line in open(filepath).readlines()]
    except FileNotFoundError:
        print(f'File {filepath} not found.')
        sys.exit(2)
    data = {}
    description = {}
    date = None
    for line in filecontent:
        if line.startswith('###'):
            date = re.match(date_re, line).group(1)
        else:
            matches = re.match(data_re, line)
            if matches is None:
                continue
            ticker, descr, price = matches.groups()
            if date is not None:
                if ticker not in description.keys():
                    description[ticker] = descr
                if ticker in data.keys():
                    data[ticker].append((date, float(price.replace(',', '.'))))
                else:
                    data[ticker] = [(date, float(price.replace(',', '.')))]
    fig, ax = pl.subplots()
    if len(data.keys()) == 0:
        print(f'No ticker data found in file {filepath}.')
        sys.exit(3)
    for ticker in data.keys():
        xticks, y = map(list, zip(*data[ticker]))
        x = [datetime.datetime.strptime(s, "%d.%m.%y").timestamp() for s in xticks]
        
        pl.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize='x-small')  # rotate x axis labels by 45 degrees
        pl.xticks(x, xticks)  # set x tick labels, x is a list of unix timestamps, xticks is a list of readable dates
        ax.scatter(x, y, label=f'{ticker} - {description[ticker]}')  # create a scatter plot, plot only dots
        ax.plot(x, y)  # create a line chart, connect the dots
        ax.legend(frameon=False)  # no frame around the legend
        ax.yaxis.set_minor_locator(AutoMinorLocator(10))  # have ten minor ticks between two major ticks
        ax.grid(axis='y', which='major', color='#dddddd', linestyle='--')  # major tick lines are dashed
        ax.grid(axis='y', which='minor', color='#dddddd', linestyle=':')  # minor tick lines are dotted
    mplcursors.cursor(hover=True)
    pl.show()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} /path/to/file')
        sys.exit(1)
    main()
