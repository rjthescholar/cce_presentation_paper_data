#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import math as mth
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Filename to plot")
    args = parser.parse_args(sys.argv[1:])
    infile = f'./{args.filename}.txt'
    outfile = f'./{args.filename}.png'

    with open(infile, 'r') as f:
        data = [int(line.rstrip("\n")) for line in f if line.strip()]

    fig = plt.figure(figsize =(5, 2))
    xlbl,  ylbl = args.filename.split("-per-")
    plt.xlabel(xlbl.replace("-", " ").title())
    plt.title(f'{xlbl.replace("-", " ").title()} Per {ylbl.title()}')
    plt.gca().axes.get_yaxis().set_visible(False)

    plt.boxplot(data, vert=False, notch=False)
    plt.savefig(outfile)

    print(f"Total: {sum(data)}")
    print(f"Avg: {sum(data)/len(data)}")
