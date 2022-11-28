import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def head(input, output, args):
    if len(args) != 1 and len(args) != 3:
        raise ValueError("wrong number of command line arguments")
    if len(args) == 1:
        num_lines = 10
        file = args[0]
    if len(args) == 3:
        if args[0] != "-n":
            raise ValueError("wrong flags")
        else:
            num_lines = int(args[1])
            file = args[2]
    with open(file) as f:
        lines = f.readlines()
        for i in range(0, min(len(lines), num_lines)):
            output.append(lines[i])
