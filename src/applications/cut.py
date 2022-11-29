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
    indexs = []
    file = args[2]

    with open(file) as f:
        lines = f.readlines()

        for byte in bytes:
            if "-" not in byte:
                if (int(byte) - 1) not in indexs:
                    indexs.append(int(byte) - 1)
            elif byte[0] == "-":
                for i in range(0, int(byte[1:])):
                    if i not in indexs:
                        indexs.append(i)
            elif byte[-1] == "-":
                for i in range(int(byte[:-1]) - 1, len(max(lines, key=len))):
                    if i not in indexs:
                        indexs.append(i)
            else:
                indexRange = byte.split("-")
                for i in range(int(indexRange[0]) - 1, int(indexRange[1])):
                    if i not in indexs:
                        indexs.append(i)

        indexs.sort()

        for line in lines:
            line = line.strip("\n")
            newLine = ""
            for i in indexs:
                if i < len(line):
                    newLine = newLine + line[i]
            output.append(newLine + "\n")
