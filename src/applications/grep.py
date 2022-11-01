import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def grep(cmdline, out, args):
    if len(args) < 2:
        raise ValueError("wrong number of command line arguments")
    pattern = args[0]
    files = args[1:]
    for file in files:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(pattern, line):
                    if len(files) > 1:
                        out.append(f"{file}:{line}")
                    else:
                        out.append(line)
