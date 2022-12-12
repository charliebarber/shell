import os
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

#General template for how a unit test should be created (I think...)
"""
class TestFunction(unittest.TestCase):
    def setUp(self) -> None:
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
# class TestShell(unittest.TestCase):
#     def test_shell(self):
#         out = deque()
#         eval("echo foo", out)
#         self.assertEqual(out.popleft(), "foo\n")
#         self.assertEqual(len(out), 0)


"""HELPER FUNCTIONS"""
def get_output(cmd: str) -> str:
    """
    This is a helper function which formats the output of single lines
    in a way that is easier for assertEqual to interpret
    """

    return "".join(eval(cmd)) 


class TestPwd(unittest.TestCase):
    def setUp(self) -> None:
        self.pwd = Pwd(False)
        self.unsafe_pwd = Pwd(True)
"""
    def test_pwd(self):
        args = []
        output = self.pwd.exec(args).strip().split('\n')
        self.assertEqual(output, ["/comp0010"])

    def test_unsafe_pwd(self):
        args = []
        output = self.unsafe_pwd.exec(args).strip().split('\n')
        self.assertEqual(output, ["/comp0010"])

    def test_unsafe_pwd_error(self):
        args = []
        output = self.unsafe_pwd.exec(args).strip().split('\n')
"""


class TestCd(unittest.TestCase):
    def setUp(self) -> None:
        self.Cd = Cd

    def test_cd_dummy(self):
        pass


class TestLs(unittest.TestCase):
    def setUp(self) -> None:
        self.Ls = Ls

    def test_ls_dummy(self):
        pass


class TestCat(unittest.TestCase):
    def setUp(self) -> None:
        self.Cat = Cat

    def test_cat_dummy(self):
        pass


class TestEcho(unittest.TestCase):
    def setUp(self) -> None:
        self.Echo = Echo

    def test_echo_dummy(self):
        pass


class TestHead(unittest.TestCase):
    def setUp(self) -> None:
        self.Head = Head

    def test_head_dummy(self):
        pass


class TestTail(unittest.TestCase):
    def setUp(self) -> None:
        self.Tail = Tail

    def test_tail_dummy(self):
        pass


class TestGrep(unittest.TestCase):
    def setUp(self) -> None:
        self.Grep = Grep

    def test_grep_dummy(self):
        pass


class TestCut(unittest.TestCase):
    def setUp(self) -> None:
        self.Cut = Cut

    def test_cut_dummy(self):
        pass


class TestFind(unittest.TestCase):
    def setUp(self) -> None:
        self.find = Find(False)
        self.unsafe_find = Find(True)
        os.chdir("/comp0010/test/test_dir/")

    def test_find(self):
        args = ["-name", "file.txt"]
        output = self.find.exec(args)
        print(output)
        self.assertEqual(output, ["./dir2/subdir/file.txt"])


class TestUniq(unittest.TestCase):
    def setUp(self) -> None:
        self.Uniq = Uniq

    def test_uniq_dummy(self):
        pass


class TestSort(unittest.TestCase):
    def setUp(self) -> None:
        self.Sort = Sort

    def test_sort_dummy(self):
        pass


class TestCompleter(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_autocomplete_dummy(self):
        pass
        

class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_parser_dummy(self):
        pass

class TestSubstitution(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_simple_substitution(self):
        out = get_output("echo `echo test`")
        self.assertEqual(out, "test\n")

    def test_seq_substitution(self):
        out = get_output("echo `echo hello; echo world`")
        self.assertEqual(out, "hello world\n")

    def test_app_substitution(self):
        out = get_output("`echo echo` test")
        self.assertEqual(out, "test\n")

    def test_failed_substitution(self):
        out = get_output("echo `echo test")
        self.assertEqual(out, "`echo test\n")

    def test_dquotes_substitution(self):
        out = get_output('echo "`echo test`"')
        self.assertEqual(out, "test\n")

if __name__ == "__main__":
    unittest.main()
