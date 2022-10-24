import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def cat(cmdline, out, args):
    for a in args:
        with open(a) as f:
            out.append(f.read())
