import re
import os
from os import listdir
import glob

from abc import ABC, abstractmethod
from typing import List


class Application(ABC):
    """
    Application is an abstract base class for all applications to inherit from
    It takes in arguments and returns the output ready for the output stream
    """

    @abstractmethod
    def exec(self, args) -> List[str]:
        pass

    def raise_error(self, message, type, output) -> None:
        if self.unsafe:
            output.append(message + "\n")
        else:
            if type == "file_not_found":
                raise FileNotFoundError(message)
            elif type == "not_directory":
                raise NotADirectoryError(message)
            elif type == "value":
                raise ValueError(message)
            elif type == "type":
                raise TypeError(message)
            else:
                raise RuntimeError(message)


class Pwd(Application):
    """
    Pwd implements the 'pwd' shell function
    It outputs the current working directory followed by a newline.
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> str:
        return os.getcwd() + "\n"


class Cd(Application):
    """
    Cd implements the 'cd' shell function
    It changes the current working directory.
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        if len(args) == 0 or len(args) > 1:
            self.raise_error(
                "Wrong number of command line arguments", "type", output
                )
        if not os.path.exists(args[0]):
            self.raise_error(
                f"No such directory: {args[0]}", "not_directory", output
                )
        else:
            os.chdir(args[0])

        return output


class Ls(Application):
    """
    Ls implements the 'ls' shell function
    Lists the content of a directory.
    It prints list of files and directories
    separated by tabs and followed by a newline.
    Ignores files and directories whose names start with '.' .
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            self.raise_error(
                "Wrong number of command line arguments", "type", output
                )
            ls_dir = args[0]
        else:
            ls_dir = args[0]
        if not os.path.exists(ls_dir):
            self.raise_error(
                f"No such directory: {ls_dir}", "not_directory", output
                )
        else:
            for f in listdir(ls_dir):
                if not f.startswith("."):
                    output.append(f + "\n")

        return output


class Cat(Application):
    """
    Cat implements the 'cat' shell function
    It concatenates the content of given files
    and prints to stdout
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        for a in args:
            if "#STDIN#" in a:
                f = a[1:]
                for x in f:
                    output.append(x)
            else:
                if not os.path.exists(a):
                    self.raise_error(
                        f"No such file or directory: {a}",
                        "file_not_found",
                        output
                    )
                else:
                    with open(a) as f:
                        output.append(f.read())

        return output


class Echo(Application):
    """
    Echo implements the 'echo' shell function
    It prints its args seperated by spaces
     and followed by newline to stdout
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> str:
        return " ".join(args) + "\n"


class Head(Application):
    """
    Head implements the 'head' shell function
    Prints the first N lines of a given file or stdin
    If < N lines, it prints only existing lines without raising an exception
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        file = ""

        if len(args) != 1 and len(args) != 3:
            self.raise_error(
                "Wrong number of command line arguments", "type", output
                )
            return output
        if len(args) == 1:
            num_lines = 10
            file = args[0]
        if len(args) == 3:
            if args[0] != "-n":
                self.raise_error(
                    "Wrong flags", "value", output
                    )
                return output
            else:
                num_lines = int(args[1])
                file = args[2]

        if "#STDIN#" in file:
            file = file[1]
            lines = file.split("\n")
            for i in range(0, min(len(lines), num_lines)):
                output.append(lines[i] + "\n")
        else:
            if not os.path.exists(file):
                self.raise_error(
                    f"No such file or directory: {file}",
                    "file_not_found",
                    output
                )
            else:
                with open(file) as f:
                    lines = f.readlines()
                    for i in range(0, min(len(lines), num_lines)):
                        if i == len(lines) - 1:
                            output.append(lines[i] + "\n")
                        else:
                            output.append(lines[i])

        return output


class Tail(Application):
    """
    Tail implements the 'tail' shell function
    Prints the last N lines of a given file or stdin
    If < N lines, it prints only existing lines
     without raising an exception
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        file = ""

        if len(args) != 1 and len(args) != 3:
            self.raise_error(
                "Wrong number of command line arguments",
                "type",
                output
                )
            return output
        if len(args) == 1:
            num_lines = 10
            file = args[0]
        if len(args) == 3:
            if args[0] != "-n":
                self.raise_error(
                    "Wrong flags", "value", output
                    )
                return output
            else:
                num_lines = int(args[1])
                file = args[2]

        if "#STDIN#" in file:
            file = file[1]
            lines = file.split("\n")
            display_length = min(len(lines), num_lines) + 1
            for i in range(0, display_length):
                output.append(lines[len(lines) - display_length + i] + "\n")
        else:
            if not os.path.exists(file):
                self.raise_error(
                    f"No such file or directory: {file}",
                    "file_not_found",
                    output
                )
            else:
                with open(file) as f:
                    lines = f.readlines()
                    display_length = min(len(lines), num_lines)
                    for i in range(0, display_length):
                        if i == display_length - 1:
                            output.append(lines[len(lines) - display_length + i] + "\n")
                        else:
                            output.append(lines[len(lines) - display_length + i])

        return output


class Grep(Application):
    """
    Grep implements the 'grep' shell function
    It searches for lines containing a match to specified pattern
    Output of command is the list of lines found
    Each line is followed by a newline
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        if len(args) < 2:
            self.raise_error(
                "Wrong number of command line arguments",
                "type",
                output
                )
            return output

        pattern = args[0]
        files = args[1:]
        for file in files:
            if "#STDIN#" in file:
                file = file[1]
                for line in file.split("\n"):
                    if line != "":
                        if re.match(pattern, line):
                            output.append(line + "\n")
            else:
                if not os.path.exists(file):
                    self.raise_error(
                        f"No such file or directory: {file}",
                        "file_not_found",
                        output
                    )
                else:
                    with open(file) as f:
                        lines = f.readlines()
                        for line in lines:
                            if re.match(pattern, line):
                                if len(files) > 1:
                                    output.append(f"{file}:{line}")
                                else:
                                    output.append(line)

        return output


class Cut(Application):
    """
    Cut implements the 'cut' shell function
    It cuts out sections from each line of a given file or stdin
    Outputs result to stdout
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        if len(args) != 3:
            self.raise_error(
                "Wrong number of command line arguments",
                "type",
                output
                )
            return output
        if args[0] != "-b":
            self.raise_error(
                "Wrong flags", "value", output
                )
            return output

        bytes = args[1].split(",")
        indexs = []
        file = args[2]

        if "#STDIN#" in file:
            file = file[1]
            lines = file.split("\n")
        else:
            if not os.path.exists(file):
                self.raise_error(
                    f"No such file or directory: {file}",
                    "file_not_found",
                    output
                )
            else:
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

        return output


class Find(Application):
    """
    Find implements the 'find' shell function
    It recursively searches for files with matching names
    Outputs list of relative paths, each followed by newline
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []
        initPathLength = len(os.getcwd())
        path = args[0]

        def recursive_find(path):
            files = os.listdir(path)
            for file in files:
                newPath = os.path.join(path, file)
                if args[0] != "-name":
                    # outputs absolute path if directory is given at the start
                    output.append(newPath + "\n")
                elif args[0] == "-name":
                    # replace absolute path with relative path if no dir given
                    output.append("." + newPath[initPathLength:] + "\n")

                if os.path.isdir(newPath):
                    recursive_find(newPath)

        # If no directory is given, use current working directory
        if args[0] == "-name":
            path = os.getcwd()
        if args[0] != "-name" and not os.path.exists(args[0]):
            self.raise_error(
                "directory given does not exist",
                "not_directory",
                output
                )
            return output
        if "-name" not in args:
            recursive_find(path)
        if args[len(args) - 1] == "-name":
            self.raise_error(
                "-name requires additional arguments",
                "type",
                output
                )
            return output

        # If globbing wildcard is given, this runs instead.
        elif len(args) > 1:
            s = args[len(args) - 1]
            concPath = path + "/**/" + s
            files = glob.glob(concPath, recursive=True)
            if args[0] != "-name":
                for file in files:
                    output.append(file + "\n")
            elif args[0] == "-name":
                for file in files:
                    output.append("." + file[initPathLength:] + "\n")

        return output


class Uniq(Application):
    """
    Uniq implements the 'uniq' shell function
    It detects and deletes adjacent duplicate lines from an input file/stdin
    Outputs result to stdout
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []

        if len(args) > 2:
            self.raise_error(
                "Wrong number of command line arguments",
                "type",
                output
                )
            return output
        if len(args) == 1:
            file = args[0]
            case = 0
        if len(args) == 2:
            if args[0] != "-i":
                self.raise_error("Wrong flags", "value", output)
                return output
            else:
                case = 1
                file = args[1]

        if "#STDIN#" in file:
            contents = []
            for lines in file[1:]:
                for line in lines.split("\n"):
                    if line != "":
                        contents.append(line)
        else:
            if not os.path.exists(file):
                self.raise_error(
                    f"No such file or directory: {file}",
                    "file_not_found",
                    output
                )
                return output
            else:
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
                while ((j + 1) < len(contents) and
                        contents[j].lower() == contents[
                    j + 1
                ].lower()):
                    if (j + 1) not in indexToRemove:
                        indexToRemove.append(j + 1)
                    j += 1

        indexToRemove.sort(reverse=True)

        for index in indexToRemove:
            contents.pop(index)

        for line in contents:
            output.append(line + "\n")

        return output


# TODO Implement sort from Robins branch
class Sort(Application):
    """
    Sort implements the 'sort' shell function
    It sorts the contents of a file/stdin line by line
    Outputs results to stdout
    """

    def __init__(self, unsafe) -> None:
        self.unsafe = unsafe

    def exec(self, args) -> List[str]:
        output = []

        rev = 0  # reverse order true/false
        if len(args) > 2:
            self.raise_error(
                "Wrong number of command line arguments",
                "type",
                output
                )
            return output
        if len(args) == 1:
            file = args[0]
        if len(args) == 2:
            if args[0] != "-r":
                self.raise_error(
                    "Wrong flags",
                    "value",
                    output
                    )
                return output
            else:
                rev = 1
                file = args[1]

        if "#STDIN#" in file:
            contents = []
            for lines in file[1:]:
                for line in lines.split("\n"):
                    if line != "":
                        contents.append(line)
        else:
            if not os.path.exists(file):
                self.raise_error(
                    f"No such file or directory: {file}",
                    "file_not_found",
                    output
                )
                return output
            else:
                with open(file, "r") as f:
                    contents = f.read().splitlines()

        contents.sort()
        if rev == 1:
            contents = contents[::-1]

        for line in contents:
            output.append(line + "\n")

        return output
