import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def cd(cmdline, out, args):
    if len(args) == 0 or len(args) > 1:
        raise ValueError("wrong number of command line arguments")
    os.chdir(args[0])
