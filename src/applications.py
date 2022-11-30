import re
import sys
import os
from os import listdir
from collections import deque
from glob import glob

from abc import ABC, abstractmethod

class Application(ABC):
    """"
    Application is an abstract base class for all applications to inherit from
    """

    @abstractmethod
    def exec(self, args, input, output) -> None:
        pass


class UnsafeDecorator():
    """
    UnsafeDecorator ....
    """

    def __init__(self, app) -> None:
        self.app = app

    def exec(self, args, input, output) -> None:
        pass


class Pwd(Application):
    """
    Pwd implements the 'pwd' shell function
    It outputs the current working directory followed by a newline.
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        print("called with", os.getcwd())
        output.append(os.getcwd())


# TODO Fix error handling in Cd class - type hints
class Cd(Application):
    """
    Cd implements the 'cd' shell function
    It changes the current working directory.
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        if len(args) == 0 or len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(args[0]) 


class Ls(Application):
    """
    Ls implements the 'ls' shell function
    Lists the content of a directory. 
    It prints list of files and directories separated by tabs and followed by a newline. 
    Ignores files and directories whose names start with '.' .
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]
        for f in listdir(ls_dir):
            if not f.startswith("."):
                output.append(f + "\n")


class Cat(Application):
    """
    Cat implements the 'cat' shell function
    It concatenates the content of given files and prints to stdout
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        for a in args:
            with open(a) as f:
                output.append(f.read())


class Echo(Application):
    """
    Echo implements the 'echo' shell function
    It prints its args seperated by spaces and followed by newline to stdout
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        output.append(" ".join(args) + "\n")


class Head(Application):
    """
    Head implements the 'head' shell function
    Prints the first N lines of a given file or stdin
    If < N lines, it prints only existing lines without raising an exception
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
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


class Tail(Application):
    """
    Tail implements the 'tail' shell function
    Prints the last N lines of a given file or stdin
    If < N lines, it prints only existing lines without raising an exception
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
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
            display_length = min(len(lines), num_lines)
            for i in range(0, display_length):
                output.append(lines[len(lines) - display_length + i])


class Grep(Application):
    """
    Grep implements the 'grep' shell function
    It searches for lines containing a match to specified pattern
    Output of command is the list of lines found
    Each line is followed by a newline
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:
        if len(args) < 2:
            raise ValueError("wrong number of command line arguments")
        pattern = args[0]
        files = args[1:]
        for file in files:
            with open(file) as f:
                lines = f.readlines()
                for line in lines:
                    if re.match(pattern, line):
                        if len(files) > 1:
                            output.append(f"{file}:{line}")
                        else:
                            output.append(line)


# TODO Implement cut from Alistairs branch
class Cut(Application):
    """
    Cut implements the 'cut' shell function
    It cuts out sections from each line of a given file or stdin
    Outputs result to stdout
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:    
        pass


# TODO Implement find from Robins branch
class Find(Application):
    """
    Find implements the 'find' shell function
    It recursively searches for files with matching names
    Outputs list of relative paths, each followed by newline 
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:    
        pass


# TODO Implement Uniq from Alistairs branch
class Uniq(Application):
    """
    Uniq implements the 'uniq' shell function
    It detects and deletes adjacent duplicate lines from an input file/stdin
    Outputs result to stdout
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:    
        pass


# TODO Implement sort from Robins branch
class Sort(Application):
    """
    Sort implements the 'sort' shell function
    It sorts the contents of a file/stdin line by line
    Outputs results to stdout
    """

    def __init__(self) -> None:
        pass

    def exec(self, args, input, output) -> None:    
        pass