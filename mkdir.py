#!/usr/bin/env python3
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('dir_name', help="name_s of directories", nargs='*', default=None)
parser.add_argument('-p', '--parents', help="no error if existing", action='store_true')
args = parser.parse_args()
dirs = args.dir_name
if len(dirs) == 0:
    sys.stdout.write("mkdir: missing operand \n Try mkdir --help for more information.")
else:
    for dir in dirs:
        if os.path.exists(dir):
            if args.parents:
                pass
            else:
                sys.stdout.write(f"mkdir: cannot create directory '{dir}': File exists")
        else:
            os.mkdir(dir)
