import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def echo(cmdline, out, args):
    out.append(" ".join(args) + "\n")
