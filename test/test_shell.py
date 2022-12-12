import os
from pyclbr import Function
import unittest

from shell import eval
from collections import deque
from typing import List

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

<<<<<<< HEAD
#General template for how a unit test should be created (I think...)
=======
# General template for how a unit test should be created (I think...)
>>>>>>> d5b01a51666cbec3f69eba41e49b12b5cd77f898
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


def format_output(output: List[str]) -> List[str]:
    """
    This is a helper function which formats the output of single lines
    in a way that is easier for assertEqual to interpret
    """

    string = ""
    for item in output:
        string = string + item

    return list(filter(None, string.split("\n")))


class TestPwd(unittest.TestCase):
    def setUp(self) -> None:
        self.pwd = Pwd(False)
        self.unsafe_pwd = Pwd(True)
"""
    def test_pwd(self):
        args = []
        output = self.pwd.exec(args)
        self.assertEqual(output, "/comp0010\n")

    def test_unsafe_pwd(self):
        args = []
        output = self.unsafe_pwd.exec(args)
        self.assertEqual(output, "/comp0010\n")

    def test_unsafe_pwd_error(self):
        args = []
<<<<<<< HEAD
        output = self.unsafe_pwd.exec(args).strip().split('\n')
"""
=======
        output = self.unsafe_pwd.exec(args)
>>>>>>> d5b01a51666cbec3f69eba41e49b12b5cd77f898


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
        self.echo = Echo(False)
        self.unsafe_echo = Echo(True)

    def test_echo(self):
        args = ["Hello World!"]
        output = self.echo.exec(args)
        self.assertEqual(output, "Hello World!\n")

    """def test_echo_multi_arg(self):
        args = ["Hello", "World!"]
        output = self.echo.exec(args)
        self.assertEqual(output, "Hello World!\n")"""


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
        self.uniq = Uniq(False)
        self.unsafe_uniq = Uniq(True)

    def test_uniq_case(self):
        args = ["/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt"]
        output = format_output(self.uniq.exec(args))
        self.assertEqual(output, ["AAA", "aaa", "AAA"])

    def test_uniq_no_case(self):
        args = ["/comp0010/test/test_dir/test_dir2/test_subdir/test_file4.txt"]
        output = format_output(self.uniq.exec(args))
        self.assertEqual(output, ["AAA", "BBB", "CCC", "BBB", "AAA"])

    def test_uniq_i(self):
        args = ["-i", "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt"]
        output = format_output(self.uniq.exec(args))
        self.assertEqual(output, ["AAA"])

    def test_uniq_stdin(self):
        args = [["#STDIN#", "AAA\naaa\nAAA\n"]]
        output = format_output(self.uniq.exec(args))
        self.assertEqual(output, ["AAA", "aaa", "AAA"])

    def test_uniq_stdin_i(self):
        args = ["-i", ["#STDIN#", "AAA\naaa\nAAA\n"]]
        output = format_output(self.uniq.exec(args))
        self.assertEqual(output, ["AAA"])

    def test_uniq_extra_arg_error(self):
        args = [
            "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
            "test_arg",
            "test_arg",
        ]
        with self.assertRaises(TypeError):
            self.uniq.exec(args)

    def test_uniq_wrong_arg_error(self):
        args = [
            "test_arg",
            "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
        ]
        with self.assertRaises(ValueError):
            self.uniq.exec(args)

    def test_uniq_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir2/test_subdir/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.uniq.exec(args)

    def test_unsafe_uniq_extra_arg_error(self):
        args = [
            "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
            "test_arg",
            "test_arg",
        ]
        output = self.unsafe_uniq.exec(args)

    def test_unsafe_uniq_wrong_arg_error(self):
        args = [
            "test_arg",
            "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
        ]
        output = self.unsafe_uniq.exec(args)

    def test_unsafe_uniq_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir2/test_subdir/test_nofile.txt"]
        output = self.unsafe_uniq.exec(args)


class TestSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sort = Sort(False)
        self.unsafe_sort = Sort(True)

    def test_sort(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.sort.exec(args))
        self.assertEqual(output, ["AAA", "AAA", "BBB"])

    def test_sort_r(self):
        args = ["-r", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.sort.exec(args))
        self.assertEqual(output, ["BBB", "AAA", "AAA"])

    def test_sort_stdin(self):
        args = [["#STDIN#", "AAA\nAAA\nBBB\n"]]
        output = format_output(self.sort.exec(args))
        self.assertEqual(output, ["AAA", "AAA", "BBB"])

    def test_sort_wrong_arg_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file1.txt", "test_arg"]
        with self.assertRaises(ValueError):
            self.sort.exec(args)

    def test_sort_extra_arg_error(self):
        args = [
            "/comp0010/test/test_dir/test_dir1/test_file1.txt",
            "test_arg",
            "test_arg",
        ]
        with self.assertRaises(TypeError):
            self.sort.exec(args)

    def test_sort_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file3.txt"]
        with self.assertRaises(FileNotFoundError):
            self.sort.exec(args)

    def test_unsafe_sort_wrong_arg_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file1.txt", "test_arg"]
        output = self.unsafe_sort.exec(args)

    def test_unsafe_sort_extra_arg_error(self):
        args = [
            "/comp0010/test/test_dir/test_dir1/test_file1.txt",
            "test_arg",
            "test_arg",
        ]
        output = self.unsafe_sort.exec(args)

    def test_unsafe_sort_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file3.txt"]
        output = self.unsafe_sort.exec(args)


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
        output = get_output("echo `echo test`")
        self.assertEqual(output, "test\n")

    def test_seq_substitution(self):
        output = get_output("echo `echo hello; echo world`")
        self.assertEqual(output, "hello world\n")

    def test_app_substitution(self):
        output = get_output("`echo echo` test")
        self.assertEqual(output, "test\n")

    def test_failed_substitution(self):
        output = get_output("echo `echo test")
        self.assertEqual(output, "`echo test\n")

    def test_dquotes_substitution(self):
        output = get_output('echo "`echo test`"')
        self.assertEqual(output, "test\n")


if __name__ == "__main__":
    unittest.main()
