#!/usr/bin/env python3

import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default=os.getcwd())
parser.add_argument('-a', '--all', help='include hidden .files', action='store_true')
args = parser.parse_args()
directory = args.path

if os.path.exists(directory):
        if args.all:
                ls_list = os.listdir(directory)
                ls_list = " ".join(ls_list)
                sys.stdout.write(ls_list+'\n')
        else:
                all_files = os.listdir(directory)
                ls_list = [i for i in all_files if not i.startswith(".")]
                ls_list = " ".join(ls_list)
                sys.stdout.write(ls_list+'\n')
else:
        sys.stdout.write(f"ls: cannot access '{directory}': No such file or directory"'\n')
        sys.exit(0)
