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
    for m in re.finditer("[^\\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
        # print(m)
        if m.group(1) or m.group(2):
            quoted = m.group(0)
            tokens.append(quoted[1:-1])
        else:
            globbing = glob.glob(m.group(0))
            if globbing:
                tokens.extend(globbing)
            else:
                tokens.append(m.group(0))

    app = tokens[0]
    args = tokens[1:]

    return (app, args)

# def run_cmd(app, args, out):
#     application = get_application(app)
#     output_redirect_file = ""
#     if ">" in args:
#         output_redirect_file = args[args.index(">") + 1]
#         args = args[: args.index(">")]

#     app_outputs = application.exec(args, cmdline)
#     print("APP OUTPUTS", app_outputs)

#     if output_redirect_file:
#         f = open(output_redirect_file, "w")
#         for output in app_outputs:
#             f.write(output)
#     else:
#         for output in app_outputs:
#             out.append(output)
#             print("OUT", out)


def eval(cmdline, out) -> None:
    """
    eval takes in cmdline input and parses it.
    It interprets the command and runs the correct application.
    Adds output to the output queue given as an arg.
    """

    # raw_commands stores the parsed commands before interpretation
    raw_commands = []

    # Commands in sequence are added to a queue and popped in order
    seq_queue = deque()

    # Finds all commands seperated by semicolons and appends each to raw_commands
    for m in re.finditer("([^;].?[^;]+)", cmdline):
        # print(m)
        if m.group(0):
            seq_queue.append(m.group(0))

    # print(raw_commands)



    while seq_queue:
        command = seq_queue.popleft()

        if '|' in command:
            cmds = []
            # Regex to seperate by | chars
            for m in re.finditer("([^\|].?[^\|]+)", command):
                if m.group(0):
                    cmds.append(m.group(0))

            # run commands and store their output
            prev_out = []
            for i in range(len(cmds) - 1):
                app, args = eval_cmd(cmds[i])
                application = get_application(app)
                # for arg in prev_out:
                #     args.append(arg)
                if prev_out:
                    prev_out.insert(0, "#STDIN#")
                    args.append(prev_out)

                # print("args", args)
                app_outputs = application.exec(args, cmdline)
                # print("outputs", app_outputs)
                prev_out = ["".join(app_outputs)]
                # print("prev out", prev_out)

            # append the last command to seq queue
            app, args = eval_cmd(cmds[len(cmds) - 1])
            # print("app args", app, args)
            if prev_out:
                prev_out.insert(0, "#STDIN#")
                # print("newprev", prev_out) 
                args.append(prev_out)

            # seq_queue.appendleft(evaluated)
            # print(app, args)
            application = get_application(app)
            output_redirect_file = ""
            if ">" in args:
                output_redirect_file = args[args.index(">") + 1]
                args = args[: args.index(">")]

            app_outputs = application.exec(args, cmdline)
            # print("outputs", app_outputs)

            if output_redirect_file:
                f = open(output_redirect_file, "w")
                for output in app_outputs:
                    f.write(output)
            else:
                for output in app_outputs:
                    out.append(output)
            
                    
        else:
            app, args = eval_cmd(command)
            # print(app, args)

            application = get_application(app)
            output_redirect_file = ""
            if ">" in args:
                output_redirect_file = args[args.index(">") + 1]
                args = args[: args.index(">")]

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

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


if __name__ == "__main__":
    readline.set_completer_delims(' \t\n;')
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
