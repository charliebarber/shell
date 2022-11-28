import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def cat(input, output, args):
    for a in args:
        with open(a) as f:
            output.append(f.read())
