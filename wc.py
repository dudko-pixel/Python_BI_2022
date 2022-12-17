#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='+', default=sys.stdin)
parser.add_argument('-l', '--lines', action='store_true', help='Count lines')
parser.add_argument('-w', '--words', action='store_true', help='Count words')
parser.add_argument('-c', '--bites', action='store_true', help='Count bites')
args = parser.parse_args()
entry = args.infile

for file in entry:
    if os.path.exists(file):
        if args.lines:
            print(len(open(file).readlines()), end = ' ')
            if args.words:
                print(len(open(file).read().split()), end = ' ')
                if args.bites:
                    print(os.path.getsize(file), end = ' ')
            print(file)
            sys.exit(0)
        elif args.words:
            print(len(open(file).read().split()), end = ' ')
            if args.bites:
                print(os.path.getsize(file), end = ' ')
            print(file)
            sys.exit(0)
        elif args.bites:
            print(os.path.getsize(file), end = ' ')
            print(file)
            sys.exit(0)
        else:
            print(len(open(file).readlines()), len(open(file).read().split()), os.path.getsize(file), file)
    else:
        print(f"wc: cannot access '{file}': No such file or directory")
sys.exit(0)
