import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def sort(cmdline, out, args):
    rev = 0  # reverse order true/false
    if len(args) > 2:
        raise ValueError("wrong number of command line arguments")
    if len(args) == 1:
        file = args[0]
    if len(args) == 2:
        if args[0] != "-r":
            raise ValueError("wrong flags")
        else:
            rev = 1
            file = args[1]

    with open(file, "r") as f:
        contents = f.read().splitlines()

    contents.sort()
    if rev == 1:
        contents = contents[::-1]

    for line in contents:
        out.append(line + "\n")
