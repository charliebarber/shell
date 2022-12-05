import imp
import re
import sys
import os
from typing import List, Tuple
from applications.factory import get_application

from os import listdir
from collections import deque
from glob import glob
import readline


def eval_cmd(command: str) -> Tuple[str, List[str]]:
    """
    eval_cmd takes in a command string and parses it.
    It returns the app and arguments as a tuple.
    """
    tokens = []
    for m in re.finditer("[^\\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
        # print(m)
        if m.group(1) or m.group(2):
            quoted = m.group(0)
            tokens.append(quoted[1:-1])
        else:
            globbing = glob(m.group(0))
            if globbing:
                tokens.extend(globbing)
            else:
                tokens.append(m.group(0))

    app = tokens[0]
    args = tokens[1:]

    return (app, args)


def eval(cmdline, out) -> None:
    """
    eval takes in cmdline input and parses it.
    It interprets the command and runs the correct application.
    Adds output to the output queue given as an arg.
    """

    # raw_commands stores the parsed commands before interpretation
    raw_commands = []

    # Finds all commands seperated by semicolons and appends each to raw_commands
    for m in re.finditer("([^;].?[^;]+)", cmdline):
        # print(m)
        if m.group(0):
            raw_commands.append(m.group(0))

    # print(raw_commands)

    # Commands in sequence are added to a queue and popped in order
    seq_queue = deque()

    for command in raw_commands:

        # Handle pipeline commands
        # prev_output = ""
        # Regex to seperate by | chars
        # for m in re.finditer("([^\|].?[^\|]+)", command):

        evaluated = eval_cmd(command)

        # Append pair of app and its args to the sequence queue
        seq_queue.append(evaluated)

    while seq_queue:
        app, args = seq_queue.popleft()
        application = get_application(app)

        args = input_redirection(args)

        output_redirect_file = ""
        if ">" in args:
            output_redirect_file = args[args.index(">") + 1]

            args = args[: args.index(">")] + args[(args.index(">") + 2) :]
            if ">" in args:
                raise ValueError("several files are specified for output redirection")

        app_outputs = application.exec(args, cmdline)

        if output_redirect_file:
            f = open(output_redirect_file, "w")
            for output in app_outputs:
                f.write(output)
        else:
            for output in app_outputs:
                out.append(output)


def input_redirection(args: List[str]) -> List[str]:
    reformated_args = []
    for arg in args:
        if "<" in arg and arg != "<":
            split = list(filter(None, arg.split("<")))
            if len(split) > 1:
                raise ValueError("several files are specified for input redirection")
            for item in split:
                reformated_args.append("<")
                reformated_args.append(item)
        else:
            reformated_args.append(arg)

    if "<" in reformated_args:
        reformated_args = (
            reformated_args[: reformated_args.index("<")]
            + reformated_args[reformated_args.index("<") + 1 :]
        )
        if "<" in reformated_args:
            raise ValueError("several files are specified for input redirection")

    return reformated_args


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        eval(sys.argv[2], out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
