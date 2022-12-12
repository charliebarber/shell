from applications.applications import (
    Pwd,
    Cd,
    Ls,
    Cat,
    Echo,
    Head,
    Tail,
    Grep,
    Cut,
    Find,
    Uniq,
    Sort,
)


def get_application(call) -> object:
    """
    get_application follows the Factory pattern
    to create new application objects.
    It looks up the call in a dictionary
    and returns a new Application object
    """

    factory = {
        "pwd": Pwd(False),
        "cd": Cd(False),
        "ls": Ls(False),
        "cat": Cat(False),
        "echo": Echo(False),
        "head": Head(False),
        "tail": Tail(False),
        "grep": Grep(False),
        "cut": Cut(False),
        "find": Find(False),
        "uniq": Uniq(False),
        "sort": Sort(False),
        "_ls": Ls(True),
        "_pwd": Pwd(True),
        "_cd": Cd(True),
        "_cat": Cat(True),
        "_echo": Echo(True),
        "_head": Head(True),
        "_tail": Tail(True),
        "_grep": Grep(True),
        "_cut": Cut(True),
        "_find": Find(True),
        "_uniq": Uniq(True),
        "_sort": Sort(True),
    }

    # Instantiate new Application object and return it
    return factory[call]
