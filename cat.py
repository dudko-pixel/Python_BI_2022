#!/usr/bin/env python3

import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file', nargs='*', default=sys.stdin)
args = parser.parse_args()

file_in = args.input_file

if type(file_in) == str:
    file_exists = os.path.exists(file_in)
    if file_exists:
        file = open(file_in)
        data = file.read()
        print(data)
        file.close()
    else:
        sys.stdout.write(f'cat: {file_in}: No such file or directory'+"\n")
else:
    for line in sys.stdin:
        sys.stdout.write(line.strip()+"\n")
