#! /usr/bin/env python3

import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('input_file', nargs="*")
args = parser.parse_args()

sorted_lines = []

if len(args.input_file) == 0:
    for line in sys.stdin:
        sorted_lines.append(line.strip())
else:
    for file in args.input_file:
        with open(file, 'r') as target_file:
            for line in target_file.readlines():
                sorted_lines.append(line.strip())

for line in sorted(sorted(sorted_lines), key=lambda x: x.lower()):
    line = f'{line}\n'
    sys.stdout.write(line)
