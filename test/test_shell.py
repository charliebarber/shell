from pyclbr import Function
import unittest

from shell import eval
from collections import deque

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

# General template for how a unit test should be created (I think...)
"""
class TestFunction(unittest.TestCase):
    def __init__(self) -> None:
        # instantiate the test class with the required function 
        # rather than passing it through the parser
        self.Func = Func

    def test_function_property1(self):
        pass

    def test_function_property2(self):
        pass

    def test_function_property3(self):
        pass
"""
# Believe this can be removed
class TestShell(unittest.TestCase):
    def test_shell(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)


class TestPwd(unittest.TestCase):
    def __init__(self) -> None:
        self.Pwd = Pwd

    def test_pwd_dummy(self):
        pass


class TestCd(unittest.TestCase):
    def __init__(self) -> None:
        self.Cd = Cd

    def test_cd_dummy(self):
        pass


class TestLs(unittest.TestCase):
    def __init__(self) -> None:
        self.Ls = Ls

    def test_ls_dummy(self):
        pass


class TestCat(unittest.TestCase):
    def __init__(self) -> None:
        self.Cat = Cat

    def test_cat_dummy(self):
        pass


class TestEcho(unittest.TestCase):
    def __init__(self) -> None:
        self.Echo = Echo

    def test_echo_dummy(self):
        pass


class TestHead(unittest.TestCase):
    def __init__(self) -> None:
        self.Head = Head

    def test_head_dummy(self):
        pass


class TestTail(unittest.TestCase):
    def __init__(self) -> None:
        self.Tail = Tail

    def test_tail_dummy(self):
        pass


class TestGrep(unittest.TestCase):
    def __init__(self) -> None:
        self.Grep = Grep

    def test_grep_dummy(self):
        pass


class TestCut(unittest.TestCase):
    def __init__(self) -> None:
        self.Cut = Cut

    def test_cut_dummy(self):
        pass


class TestFind(unittest.TestCase):
    def __init__(self) -> None:
        self.Find = Find

    def test_find_dummy(self):
        pass


class TestUniq(unittest.TestCase):
    def __init__(self) -> None:
        self.Uniq = Uniq

    def test_uniq_dummy(self):
        pass


class TestSort(unittest.TestCase):
    def __init__(self) -> None:
        self.Sort = Sort(False)

    def test_sort_(self):
        args = ["test/test_dir1/test_file1.txt"]
        result = self.Sort.exec(args, "")
        self.assertEqual(result, ["AAA", "AAA", "BBB"])


class TestCompleter(unittest.TestCase):
    def __init__(self) -> None:
        pass

    def test_autocomplete_dummy(self):
        pass


class TestParser(unittest.TestCase):
    def __init__(self) -> None:
        pass

    def test_parser_dummy(self):
        pass


if __name__ == "__main__":
    unittest.main()
