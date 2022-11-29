import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob


def cut(input, output, args):
    if len(args) != 3:
        raise ValueError("wrong number of command line arguments")
    if args[0] != "-b":
        raise ValueError("wrong flags")

    bytes = args[1].split(",")
    file = args[2]

    with open(file) as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i].strip("\n")
            newLine = ""
            for byte in bytes:
                if "-" not in byte:
                    if int(byte) > len(line):
                        break
                    else:
                        newLine = newLine + line[int(byte) - 1]
                elif byte[0] == "-":
                    newLine = newLine + line[: int(byte[1:])]
                elif byte[-1] == "-":
                    newLine = newLine + line[int(byte[:-1]) - 1 :]
                else:
                    indexRange = byte.split("-")
                    newLine = (
                        newLine + line[int(indexRange[0]) - 1 : (int(indexRange[1]))]
                    )

            output.append(newLine + "\n")
