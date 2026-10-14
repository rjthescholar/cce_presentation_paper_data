#!/usr/bin/env python

import os
from pathlib import Path
import argparse
import csv
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "File Input", type=Path)
    parser.add_argument("-o", "--out", help = "Concept Output", type=Path)
    args = parser.parse_args(sys.argv[1:])

    concepts = set()
    if args.file:
        with open(args.file, 'r', newline='') as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                concepts.update(row['keywords'].split(';'))

    if args.out:
        with open(args.out, 'w') as f:
            for concept in concepts:
                f.write(concept+"\n")
        
                
