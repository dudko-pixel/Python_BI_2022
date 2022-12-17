#!/usr/bin/env python3

import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--recurs', help='remove recursively', action='store_true')
parser.add_argument('path', nargs='?')
args = parser.parse_args()
file_to_remove = args.path

if file_to_remove is None:
    sys.stdout.write(f"rm: missing operand \nTry rm --help for more information.")
    sys.exit(0)
if os.path.exists(file_to_remove):
    if os.path.isfile(file_to_remove):
        os.remove(file_to_remove)
    else:
        if args.recurs is None:
            sys.stdout.write(f"rm: cannot remove '{file_to_remove}': Is a directory")
        else:
            shutil.rmtree(file_to_remove)
else:
    sys.stdout.write(f"rm: cannot remove '{file_to_remove}': No such file or directory" + '\n')
