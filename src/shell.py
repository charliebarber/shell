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
    for m in re.finditer(r"(([^\"\s]*)(\"([^\"]*)\")([^\"\s]*))|[^\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
        # If matches command splitting regex, get rid of double quotes
        if re.search(r"(([^\"\s]*)(\"([^\"]*)\")([^\"\s]*))", m.group(0)):
            tokens.append(m.group(0).replace('"', ''))
        elif m.group(7) or m.group(7):
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


def run_cmd(command, out, stdinargs=None) -> deque():
    """
    run_cmd finds the relevant application in the factory.
    It then executes it with the correct args.
    """
    # Parse command into an app and its args
    if stdinargs:
        app = command
        args = stdinargs
    else:
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

    app_outputs = application.exec(args)

    # Write output to file if provided
    # Else, append to stdout
    if output_redirect_file:
        f = open(output_redirect_file, "w")
        for output in app_outputs:
            f.write(output)
        # return None
    else:
        for output in app_outputs:
            out.append(output)

    return out


def get_sequence(command: str) -> deque:
    """
    get_sequence seperated the cmdline input by semicolons.
    It puts the commands into the correct order in a queue.
    Returns the queue.
    """

    q = deque()
    # Finds all commands seperated by semicolons
    for m in re.split(r'; (?=(?:"[^"]*?(?: [^"]*)*))|; (?=[^",]+(?:;|$))', command):
        q.append(m)

    return q


def seperate_pipes(command: str) -> List[str]:
    """
    Seperate pipeline commands and return a list
    """
    cmds = []
    # Regex to seperate by | chars
    for m in re.finditer(r"([^\|].?[^\|]+)", command):
        if m.group(0):
            cmds.append(m.group(0))

    return cmds


def input_redirection(args: List[str]) -> List[str]:
    """
    Takes current arguments and reformats to STDIN convention if there is input redirection required
    """
    reformated_args = []
    for arg in args:
        if "<" in arg and arg != "<":
            split = list(filter(None, arg.split("<")))
            if len(split) > 1:
                raise TypeError("Several files are specified for input redirection")
            for item in split:
                reformated_args.append("<")
                reformated_args.append(item)
        else:
            reformated_args.append(arg)

    if "<" in reformated_args:
        if reformated_args.count("<") != 1:
            raise TypeError("Several files are specified for input redirection")
        else:
            filename = reformated_args[reformated_args.index("<") + 1]
            if not os.path.exists(filename):
                raise FileNotFoundError("File for input redirection does not exist")
            with open(filename, "r") as file:
                data = file.read()
            reformated_args = reformated_args[: reformated_args.index("<")]
            reformated_args.append(["#STDIN#", data])

    return reformated_args


def eval_substitution(cmdline: str) -> str:
    """
    Evaluate all command substitutions.
    Executes the commands and replaces them in cmdline with their output.
    Returns the new cmdline string.
    """
    # Find if command substitution should take place
    sub_start = cmdline.find("`")
    # If it was able to find a backquote (Start of command sub)
    if sub_start != -1:
        sub_end = cmdline.find("`", sub_start + 1)
        # If matching backquote exists
        if sub_end != -1:
            sub_cmd = cmdline[sub_start + 1:sub_end]
            quoted_sub_cmd = cmdline[sub_start:sub_end + 1]
            sub_queue = get_sequence(sub_cmd)
            output = ""
            while sub_queue:
                if output:
                    output += " " + "".join(run_cmd(sub_queue.popleft(), []))
                else:
                    output = "".join(run_cmd(sub_queue.popleft(), []))
                output = output.replace("\n", '')
            cmdline = cmdline.replace(quoted_sub_cmd, output)

    return cmdline


def eval(cmdline: str) -> deque:
    """
    eval takes in cmdline input and parses it.
    It interprets the command and runs the correct application.
    Adds output to the output queue given as an arg.
    """
    out = deque()

    # Carry out any command substitutions
    cmdline = eval_substitution(cmdline)
    # Commands in sequence are added to a queue and popped in order
    seq_queue = get_sequence(cmdline)

    # Exec each command while sequence queue is not empty
    while seq_queue:
        # Take command at head of queue
        command = seq_queue.popleft()

        # If it a pipeline command, must eval each cmd individually to store output
        if "|" in command:
            pipe_cmds = seperate_pipes(command)

            # Run commands and store their output
            prev_out = []
            for i in range(len(pipe_cmds) - 1):
                app, args = eval_cmd(pipe_cmds[i])
                application = get_application(app)
                if prev_out:
                    # STDIN flag added to allow the applications to process the stdin stream
                    prev_out.insert(0, "#STDIN#")
                    # Append the previous output to the new commands args
                    args.append(prev_out)

                app_outputs = application.exec(args)
                prev_out = ["".join(app_outputs)]

            # Append the last command to seq queue
            app, args = eval_cmd(pipe_cmds[len(pipe_cmds) - 1])

            if prev_out:
                # STDIN flag added to allow the applications to process the stdin stream
                prev_out.insert(0, "#STDIN#")
                # Append the previous output to the new commands args
                args.append(prev_out)

            run_cmd(app, out, args)
        else:
            app_outputs = run_cmd(command, out)

    return out


def complete(text, state):
    return (glob.glob(text + "*") + [None])[state]


if __name__ == "__main__":
    readline.set_completer_delims(" \t\n;")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise TypeError("Wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"Unexpected command line argument {sys.argv[1]}")
        # out = deque()
        out = eval(sys.argv[2])
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            # out = deque()
            out = eval(cmdline)
            while len(out) > 0:
                print(out.popleft(), end="")
