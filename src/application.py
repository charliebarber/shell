from applications.pwd import pwd
from applications.cd import cd
from applications.echo import echo
from applications.ls import ls
from applications.cat import cat
from applications.head import head
from applications.sort import sort
from applications.tail import tail
from applications.grep import grep


class Application:
    def __init__(self):
        pass

    def exec(self, args, input, output, app):
        if app == "pwd":
            pwd(input, output, args)
        elif app == "cd":
            cd(input, output, args)
        elif app == "echo":
            echo(input, output, args)
        elif app == "ls":
            ls(input, output, args)
        elif app == "cat":
            cat(input, output, args)
        elif app == "head":
            head(input, output, args)
        elif app == "tail":
            tail(input, output, args)
        elif app == "grep":
            grep(input, output, args)
        elif app == "sort":
            sort(input, output, args)
        else:
            raise ValueError(f"unsupported application {app}")
