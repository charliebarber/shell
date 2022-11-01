import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def ls(cmdline, out, args):
    if len(args) == 0:
        ls_dir = os.getcwd()
    elif len(args) > 1:
        raise ValueError("wrong number of command line arguments")
    else:
        ls_dir = args[0]
    for f in listdir(ls_dir):
        if not f.startswith("."):
            out.append(f + "\n")
