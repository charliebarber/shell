import imp
import re
import sys
import os
from typing import List, Tuple
from applications.factory import get_application

from os import listdir
from collections import deque
import glob
import readline


def eval_cmd(command: str) -> Tuple[str, List[str]]:
    """
    eval_cmd takes in a command string and parses it.
    It returns the app and arguments as a tuple.
    """
    tokens = []
    for m in re.finditer("(([^\"\s]*)(\"([^\"]*)\")([^\"\s]*))|[^\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
        # print("m", m)
        # print("group 0", m.group(0))
        # If matches command splitting regex
        if re.search("(([^\"\s]*)(\"([^\"]*)\")([^\"\s]*))", m.group(0)):
            # print("command split found", re.search("(([^\"\s]*)(\"([^\"]*)\")([^\"\s]*))", m.group(0)))
            tokens.append(m.group(0).replace('"', ''))
        elif m.group(1) or m.group(2):
            # print("group 1", m.group(1))
            quoted = m.group(0)
            tokens.append(quoted[1:-1])
        else:
            globbing = glob.glob(m.group(0))
            if globbing:
                tokens.extend(globbing)
            else:
                tokens.append(m.group(0))

    # Check for input redirection infront of command and reorder if so
    if tokens[0] == "<":
        tokens.pop(0)
        tokens.append(tokens[0])
        tokens.pop(0)
    elif "<" in tokens[0]:
        tokens.append(tokens[0].strip("<"))
        tokens.pop(0)

    app = tokens[0]
    args = tokens[1:]

    return (app, args)


def eval(cmdline, out) -> None:
    """
    eval takes in cmdline input and parses it.
    It interprets the command and runs the correct application.
    Adds output to the output queue given as an arg.
    """

    # Commands in sequence are added to a queue and popped in order
    seq_queue = deque()

    # Finds all commands seperated by semicolons and appends each to raw_commands
    for m in re.finditer("([^;].?[^;]+)", cmdline):
        if m.group(0):
            seq_queue.append(m.group(0))

    # Exec each command while sequence queue is not empty
    while seq_queue:
        # Take command at head of queue
        command = seq_queue.popleft()

        # If it a pipeline command, must eval each cmd individually to store output
        if "|" in command:
            cmds = []
            # Regex to seperate by | chars
            for m in re.finditer("([^\|].?[^\|]+)", command):
                if m.group(0):
                    cmds.append(m.group(0))

            # Run commands and store their output
            prev_out = []
            for i in range(len(cmds) - 1):
                app, args = eval_cmd(cmds[i])
                application = get_application(app)
                if prev_out:
                    # STDIN flag added to allow the applications to process the stdin stream
                    prev_out.insert(0, "#STDIN#")
                    # Append the previous output to the new commands args
                    args.append(prev_out)

                app_outputs = application.exec(args, cmdline)
                prev_out = ["".join(app_outputs)]

            # Append the last command to seq queue
            app, args = eval_cmd(cmds[len(cmds) - 1])

            if prev_out:
                # STDIN flag added to allow the applications to process the stdin stream
                prev_out.insert(0, "#STDIN#")
                # Append the previous output to the new commands args
                args.append(prev_out)

            # Fetch app from factory
            application = get_application(app)

            # Seperate output redirection from rest of command
            output_redirect_file = ""
            if ">" in args:
                output_redirect_file = args[args.index(">") + 1]
                args = args[: args.index(">")]

            # Does input direction, changing any input to STDIN convention
            args = input_redirection(args)

            app_outputs = application.exec(args, cmdline)

            # Write output to file if provided
            # Else, append to stdout
            if output_redirect_file:
                f = open(output_redirect_file, "w")
                for output in app_outputs:
                    f.write(output)
            else:
                for output in app_outputs:
                    out.append(output)

        else:
            # Parse command into an app and its args
            app, args = eval_cmd(command)
            # Fetch app from factory
            application = get_application(app)

            # Seperate output redirection from rest of command
            output_redirect_file = ""
            if ">" in args:
                output_redirect_file = args[args.index(">") + 1]
                args = args[: args.index(">")]

            # Does input direction, changing any input to STDIN convention
            args = input_redirection(args)

            app_outputs = application.exec(args, cmdline)

            # Write output to file if provided
            # Else, append to stdout
            if output_redirect_file:
                f = open(output_redirect_file, "w")
                for output in app_outputs:
                    f.write(output)
            else:
                for output in app_outputs:
                    out.append(output)


# Takes current arguments and reformats to STDIN convention if there is input redirection required
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
        if reformated_args.count("<") != 1:
            raise ValueError("Several files are specified for input redirection")
        else:
            filename = reformated_args[reformated_args.index("<") + 1]
            if not os.path.exists(filename):
                raise FileNotFoundError("File for input redirection does not exist")
            with open(filename, "r") as file:
                data = file.read()
            reformated_args = reformated_args[: reformated_args.index("<")]
            reformated_args.append(["#STDIN#", data])

    return reformated_args


def complete(text, state):
    return (glob.glob(text + "*") + [None])[state]


if __name__ == "__main__":
    readline.set_completer_delims(" \t\n;")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
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
