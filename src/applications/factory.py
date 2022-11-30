from applications.applications import Pwd, Cd, Ls, Cat, Echo, Head, Tail, Grep, Cut, Find, Uniq, Sort

def get_application(call) -> object:
    """
    get_application follows the Factory pattern to create new application objects.
    It looks up the call in a dictionary and returns a new Application object
    """

    factory = {
        "pwd": Pwd,
        "cd": Cd,
        "ls": Ls,
        "cat": Cat,
        "echo": Echo,
        "head": Head,
        "tail": Tail,
        "grep": Grep,
        "cut": Cut,
        "find": Find,
        "uniq": Uniq,
        "sort": Sort
    }

    # Instantiate new Application object and return it
    return factory[call]()