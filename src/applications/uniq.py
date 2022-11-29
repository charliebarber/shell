import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def uniq(input, output, args):
    if len(args) > 2:
        raise ValueError("wrong number of command line arguments")
    if len(args) == 1:
        file = args[0]
        case = 0
    if len(args) == 2:
        if args[0] != "-i":
            raise ValueError("wrong flags")
        else:
            case = 1
            file = args[1]

    with open(file, "r") as f:
        contents = f.read().splitlines()

    indexToRemove = []

    if case == 0:
        for i in range(0, len(contents) - 1):
            if contents[i] == contents[i + 1]:
                indexToRemove.append(i + 1)

    elif case == 1:
        for i in range(0, len(contents) - 1):
            j = i
            while (j + 1) < len(contents) and contents[j].lower() == contents[
                j + 1
            ].lower():
                if (j + 1) not in indexToRemove:
                    indexToRemove.append(j + 1)
                j += 1

    indexToRemove.sort(reverse=True)

    for index in indexToRemove:
        contents.pop(index)

    for line in contents:
        output.append(line + "\n")
