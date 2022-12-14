import os
from pyclbr import Function
import unittest

from shell import (
    eval,
    eval_cmd,
    eval_substitution,
    get_sequence,
    input_redirection,
    run_cmd,
    seperate_pipes,
)
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

# General template for how a unit test should be created (I think...)
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
        os.chdir("/comp0010")
        self.pwd = Pwd(False)
        self.unsafe_pwd = Pwd(True)

    def test_pwd(self):
        args = []
        output = format_output(self.pwd.exec(args))
        self.assertEqual(output, ["/comp0010"])

    def test_unsafe_pwd(self):
        args = []
        output = format_output(self.unsafe_pwd.exec(args))
        self.assertEqual(output, ["/comp0010"])


class TestCd(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.cd = Cd(False)
        self.unsafe_cd = Cd(True)

    def test_cd(self):
        tmp = os.getcwd()
        args = ["test"]
        self.cd.exec(args)
        self.assertEqual(os.getcwd(), "/comp0010/test")
        os.chdir(tmp)

    def test_cd_extra_arg_error(self):
        args = ["test", "test_arg"]
        with self.assertRaises(TypeError):
            self.cd.exec(args)

    def test_cd_directory_not_exists_error(self):
        args = ["no_dir"]
        with self.assertRaises(NotADirectoryError):
            self.cd.exec(args)

    def test_unsafe_cd_extra_arg_error(self):
        args = ["test", "test_arg"]
        output = self.unsafe_cd.exec(args)

    def test_unsafe_cd_directory_not_exists_error(self):
        args = ["no_dir"]
        output = self.unsafe_cd.exec(args)


class TestLs(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.ls = Ls(False)
        self.unsafe_ls = Ls(True)

    def test_ls(self):
        args = []
        output = format_output(self.ls.exec(args))
        self.assertCountEqual(
            output,
            [
                "test",
                "tools",
                "requirements.txt",
                "apps.svg",
                "sh",
                "system_test",
                "README.md",
                "src",
                "Dockerfile",
            ],
        )

    def test_ls_dir(self):
        args = ["/comp0010/test/test_dir/test_dir1/"]
        output = format_output(self.ls.exec(args))
        self.assertCountEqual(
            output,
            [
                "test_file1.txt",
                "test_file2.txt",
                "test_file_wide.txt",
                "test_file_long.txt",
            ],
        )

    def test_ls_extra_arg_error(self):
        args = ["test_arg", "test_arg"]
        with self.assertRaises(TypeError):
            self.ls.exec(args)

    def test_ls_directory_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_no_dir/"]
        with self.assertRaises(NotADirectoryError):
            self.ls.exec(args)

    def test_unsafe_ls_extra_arg_error(self):
        args = ["test_arg", "test_arg"]
        output = self.unsafe_ls.exec(args)

    def test_unsafe_ls_directory_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_no_dir/"]
        output = self.unsafe_ls.exec(args)


class TestCat(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.cat = Cat(False)
        self.unsafe_cat = Cat(True)

    def test_cat(self):
        args = [
            "/comp0010/test/test_dir/test_dir1/test_file1.txt",
            "/comp0010/test/test_dir/test_dir1/test_file2.txt",
        ]
        output = format_output(self.cat.exec(args))
        self.assertEqual(output, ["AAA", "BBB", "AAACCC"])

    def test_cat_stdin(self):
        args = [["#STDIN#", "AAA\nBBB\nAAA"]]
        output = format_output(self.cat.exec(args))
        self.assertEqual(output, ["AAA", "BBB", "AAA"])

    def test_cat_no_arg_error(self):
        args = []
        with self.assertRaises(TypeError):
            self.cat.exec(args)

    def test_cat_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.cat.exec(args)

    def test_unsafe_cat_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        output = self.unsafe_cat.exec(args)

    def test_unsafe_cat_no_arg_error(self):
        args = []
        output = self.unsafe_cat.exec(args)


class TestEcho(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.echo = Echo(False)
        self.unsafe_echo = Echo(True)

    def test_echo(self):
        args = ["Hello World!"]
        output = format_output(self.echo.exec(args))
        self.assertEqual(output, ["Hello World!"])

    def test_echo_multi_arg(self):
        args = ["Hello", "World!"]
        output = format_output(self.echo.exec(args))
        self.assertEqual(output, ["Hello World!"])


class TestHead(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.head = Head(False)
        self.unsafe_head = Head(True)

    def test_head(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.head.exec(args))
        self.assertEqual(output, [str(i) for i in range(1, 11)])

    def test_head_0(self):
        args = ["-n", "0", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.head.exec(args))
        self.assertEqual(output, [])

    def test_head_5(self):
        args = ["-n", "5", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.head.exec(args))
        self.assertEqual(output, [str(i) for i in range(1, 6)])

    def test_head_stdin(self):
        args = [["#STDIN#", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12"]]
        output = format_output(self.head.exec(args))
        self.assertEqual(output, [str(i) for i in range(1, 11)])

    def test_head_stdin_5(self):
        args = ["-n", "5", ["#STDIN#", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12"]]
        output = format_output(self.head.exec(args))
        self.assertEqual(output, [str(i) for i in range(1, 6)])

    def test_head_extra_arg_error(self):
        args = ["test_arg", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        with self.assertRaises(TypeError):
            self.head.exec(args)

    def test_head_wrong_arg_error(self):
        args = [
            "test_arg",
            "test_arg",
            "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
        ]
        with self.assertRaises(ValueError):
            self.head.exec(args)

    def test_head_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.head.exec(args)

    def test_unsafe_head_extra_arg_error(self):
        args = ["test_arg", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = self.unsafe_head.exec(args)

    def test_unsafe_head_wrong_arg_error(self):
        args = [
            "test_arg",
            "test_arg",
            "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
        ]
        output = self.unsafe_head.exec(args)

    def test_unsafe_head_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        output = self.unsafe_head.exec(args)


class TestTail(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.tail = Tail(False)
        self.unsafe_tail = Tail(True)

    def test_tail(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.tail.exec(args))
        self.assertEqual(output, [str(i) for i in range(6, 16)])

    def test_tail_0(self):
        args = ["-n", "0", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.tail.exec(args))
        self.assertEqual(output, [])

    def test_tail_5(self):
        args = ["-n", "5", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = format_output(self.tail.exec(args))
        self.assertEqual(output, [str(i) for i in range(11, 16)])

    def test_tail_stdin(self):
        args = [["#STDIN#", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12"]]
        output = format_output(self.tail.exec(args))
        self.assertEqual(output, [str(i) for i in range(2, 13)])

    def test_tail_stdin_5(self):
        args = ["-n", "5", ["#STDIN#", "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12"]]
        output = format_output(self.tail.exec(args))
        self.assertEqual(output, [str(i) for i in range(7, 13)])

    def test_tail_extra_arg_error(self):
        args = ["test_arg", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        with self.assertRaises(TypeError):
            self.tail.exec(args)

    def test_tail_wrong_arg_error(self):
        args = [
            "test_arg",
            "test_arg",
            "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
        ]
        with self.assertRaises(ValueError):
            self.tail.exec(args)

    def test_tail_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.tail.exec(args)

    def test_unsafe_tail_extra_arg_error(self):
        args = ["test_arg", "/comp0010/test/test_dir/test_dir1/test_file_long.txt"]
        output = self.unsafe_tail.exec(args)

    def test_unsafe_tail_wrong_arg_error(self):
        args = [
            "test_arg",
            "test_arg",
            "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
        ]
        output = self.unsafe_tail.exec(args)

    def test_unsafe_tail_file_not_exists_error(self):
        args = ["/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        output = self.unsafe_tail.exec(args)


class TestGrep(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.grep = Grep(False)
        self.unsafe_grep = Grep(True)

    def test_grep(self):
        args = ["AAA", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.grep.exec(args))
        self.assertEqual(output, ["AAA", "AAA"])

    def test_grep_stdin(self):
        args = ["AAA", ["#STDIN#", "AAA\nBBB\nAAA"]]
        output = format_output(self.grep.exec(args))
        self.assertEqual(output, ["AAA", "AAA"])

    def test_grep_no_matches(self):
        args = ["DDD", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.grep.exec(args))
        self.assertEqual(output, [])

    def test_grep_re(self):
        args = ["A..", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.grep.exec(args))
        self.assertEqual(output, ["AAA", "AAA"])

    def test_grep_files(self):
        args = [
            "...",
            "/comp0010/test/test_dir/test_dir1/test_file1.txt",
            "/comp0010/test/test_dir/test_dir1/test_file2.txt",
        ]
        output = format_output(self.grep.exec(args))
        self.assertEqual(
            output,
            [
                "/comp0010/test/test_dir/test_dir1/test_file1.txt:AAA",
                "/comp0010/test/test_dir/test_dir1/test_file1.txt:BBB",
                "/comp0010/test/test_dir/test_dir1/test_file1.txt:AAA",
                "/comp0010/test/test_dir/test_dir1/test_file2.txt:CCC",
            ],
        )

    def test_grep_too_few_arg_error(self):
        args = ["test_arg"]
        with self.assertRaises(TypeError):
            self.grep.exec(args)

    def test_grep_file_not_exists_error(self):
        args = ["AAA", "/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.grep.exec(args)

    def test_unsafe_grep_too_few_arg_error(self):
        args = ["test_arg"]
        output = self.unsafe_grep.exec(args)

    def test_unsafe_grep_file_not_exists_error(self):
        args = ["AAA", "/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        output = self.unsafe_grep.exec(args)


class TestCut(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.cut = Cut(False)
        self.unsafe_cut = Cut(True)

    def test_cut(self):
        args = ["-b", "1", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["A", "B", "A"])

    def test_cut_interval(self):
        args = ["-b", "1-2", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["AA", "BB", "AA"])

    def test_cut_open_interval_right(self):
        args = ["-b", "2-", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["AA", "BB", "AA"])

    def test_cut_open_interval_left(self):
        args = ["-b", "-2", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["AA", "BB", "AA"])

    def test_cut_overlapping_interval(self):
        args = ["-b", "3-6,4-9", "/comp0010/test/test_dir/test_dir1/test_file_wide.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["CDEFGHI"])

    def test_cut_overlapping_bytes(self):
        args = ["-b", "3-5,4", "/comp0010/test/test_dir/test_dir1/test_file_wide.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["CDE"])

    def test_cut_overlapping_open_interval_right(self):
        args = ["-b", "1-,2-", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["AAA", "BBB", "AAA"])

    def test_cut_overlapping_open_interval_left(self):
        args = ["-b", "-1,-2", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["AA", "BB", "AA"])

    def test_cut_stdin(self):
        args = ["-b", "2", ["#STDIN#", "AAA\nBBB\nAAA"]]
        output = format_output(self.cut.exec(args))
        self.assertEqual(output, ["A", "B", "A"])

    def test_cut_extra_arg_error(self):
        args = ["test_arg", "test_arg", "test_arg", "test_arg"]
        with self.assertRaises(TypeError):
            self.cut.exec(args)

    def test_cut_wrong_arg_error(self):
        args = ["test_arg", "test_arg", "test_arg"]
        with self.assertRaises(ValueError):
            self.cut.exec(args)

    def test_cut_file_not_exists_error(self):
        args = ["-b", "1", "/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            self.cut.exec(args)

    def test_unsafe_cut_extra_arg_error(self):
        args = ["test_arg", "test_arg", "test_arg", "test_arg"]
        output = self.unsafe_cut.exec(args)

    def test_unsafe_cut_wrong_arg_error(self):
        args = ["test_arg", "test_arg", "test_arg"]
        output = self.unsafe_cut.exec(args)

    def test_unsafe_cut_file_not_exists_error(self):
        args = ["-b", "1", "/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        output = self.unsafe_cut.exec(args)


class TestFind(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
        self.find = Find(False)
        self.unsafe_find = Find(True)

    def test_find_nodir(self):
        args = ["-name", "*.txt"]
        tmp = os.getcwd()
        os.chdir("/comp0010/test/test_dir/test_dir1")
        output = format_output(self.find.exec(args))
        os.chdir(tmp)
        self.assertCountEqual(
            output,
            [
                "./test_file1.txt",
                "./test_file2.txt",
                "./test_file_wide.txt",
                "./test_file_long.txt",
            ],
        )

    def test_find_noname(self):
        args = ["/comp0010/test/test_dir/test_dir1"]
        output = format_output(self.find.exec(args))
        self.assertCountEqual(
            output,
            [
                "/comp0010/test/test_dir/test_dir1/test_file1.txt",
                "/comp0010/test/test_dir/test_dir1/test_file2.txt",
                "/comp0010/test/test_dir/test_dir1/test_file_wide.txt",
                "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
            ],
        )

    def test_find(self):
        args = ["/comp0010/test/test_dir/", "-name", "test_file1.txt"]
        output = format_output(self.find.exec(args))
        self.assertEqual(output, ["/comp0010/test/test_dir/test_dir1/test_file1.txt"])

    def test_find_subdirs(self):
        args = ["/comp0010/test/test_dir", "-name", "*.txt"]
        output = format_output(self.find.exec(args))
        self.assertCountEqual(
            output,
            [
                "/comp0010/test/test_dir/test_dir1/test_file1.txt",
                "/comp0010/test/test_dir/test_dir1/test_file2.txt",
                "/comp0010/test/test_dir/test_dir1/test_file_wide.txt",
                "/comp0010/test/test_dir/test_dir1/test_file_long.txt",
                "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
                "/comp0010/test/test_dir/test_dir2/test_subdir/test_file4.txt",
            ],
        )

    def test_find_dir_glob(self):
        args = ["/comp0010/test/test_dir/test_dir2", "-name", "*.txt"]
        output = format_output(self.find.exec(args))
        self.assertCountEqual(
            output,
            [
                "/comp0010/test/test_dir/test_dir2/test_subdir/test_file3.txt",
                "/comp0010/test/test_dir/test_dir2/test_subdir/test_file4.txt",
            ],
        )

    def test_find_no_dir_error(self):
        args = ["/nodir", "-name", "*.txt"]
        with self.assertRaises(NotADirectoryError):
            self.find.exec(args)

    def test_find_noname_error(self):
        args = ["/comp0010/test/test_dir", "-name"]
        with self.assertRaises(TypeError):
            self.find.exec(args)

    def test_unsafe_find_no_dir_error(self):
        args = ["/nodir", "-name", "*.txt"]
        output = self.unsafe_find.exec(args)

    def test_unsafe_find_noname_error(self):
        args = ["/comp0010/test/test_dir", "-name"]
        output = self.unsafe_find.exec(args)


class TestUniq(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")
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
        os.chdir("/comp0010")
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

    def test_completer_dummy(self):
        text = "cd test_d"
        output = complete(text, 0)
        self.assertEqual(output, "ir")


class TestSubstitution(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")

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


class TestParsing(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")

    def test_get_sequence(self):
        expected = deque()
        expected.append("echo hello")
        expected.append("echo world")
        output = get_sequence("echo hello; echo world")
        self.assertEqual(output, expected)

    def test_seperate_pipes(self):
        expected = ["cat articles/text1.txt ", ' grep "Interesting String"']
        output = seperate_pipes('cat articles/text1.txt | grep "Interesting String"')
        self.assertEqual(output, expected)

    def test_eval_substitution(self):
        expected = "echo test"
        output = eval_substitution("echo `echo test`")
        self.assertEqual(output, expected)

    def test_run_cmd(self):
        expected = deque()
        for c in "test\n":
            expected.append(c)
        output = run_cmd("echo test", deque())
        self.assertEqual(output, expected)

    def test_run_cmd_stdin(self):
        expected = deque()
        for c in "hello world\n":
            expected.append(c)
        output = run_cmd("echo", deque(), ["hello", "world"])
        self.assertEqual(output, expected)

    def test_eval(self):
        expected = deque()
        for c in "test\n":
            expected.append(c)
        output = eval("echo test")
        self.assertEqual(output, expected)

    def test_eval_seq(self):
        expected = deque()
        for c in "hello\nworld\n":
            expected.append(c)
        output = eval("echo hello; echo world")
        self.assertEqual(output, expected)

    def test_eval_pipe(self):
        expected = deque(["test\n", "\n"])
        output = eval("echo test | cat")
        self.assertEqual(output, expected)

    def test_eval_pipe_for_loop(self):
        expected = deque(["test\n\n\n", "\n"])
        output = eval("echo test | cat | cat | cat")
        self.assertEqual(output, expected)

    def test_eval_cmd(self):
        expected = ("echo", ["hello", "world"])
        output = eval_cmd("echo hello world")
        self.assertEqual(expected, output)

    def test_eval_cmd_quoted(self):
        expected = ("echo", ["hello world"])
        output = eval_cmd('echo "hello world"')
        self.assertEqual(expected, output)

    def test_eval_cmd_splitting(self):
        expected = ("echo", ["abc"])
        output = eval_cmd('echo a"b"c')
        self.assertEqual(expected, output)

    def test_output_redirection(self):
        run_cmd(
            "echo",
            deque(),
            ["abc", ">", "/comp0010/test/test_dir/test_dir1/newfile.txt"],
        )
        with open("/comp0010/test/test_dir/test_dir1/newfile.txt") as f:
            lines = f.readlines()
        self.assertEqual(["abc\n"], lines)

    # TODO
    def test_eval_cmd_globbing(self):
        pass


class TestInputRedirection(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir("/comp0010")

    def test_input_redirection(self):
        output = input_redirection(
            ["test_arg", "<", "/comp0010/test/test_dir/test_dir1/test_file1.txt"]
        )
        self.assertEqual(output, ["test_arg", ["#STDIN#", "AAA\nBBB\nAAA"]])

    def test_input_redirection_no_space(self):
        output = input_redirection(
            ["test_arg", "</comp0010/test/test_dir/test_dir1/test_file1.txt"]
        )
        self.assertEqual(output, ["test_arg", ["#STDIN#", "AAA\nBBB\nAAA"]])

    def test_input_redirection_multiple_file_error(self):
        args = [
            "<",
            "/comp0010/test/test_dir/test_dir1/test_file1.txt",
            "<",
            "/comp0010/test/test_dir/test_dir1/test_file2.txt",
        ]
        with self.assertRaises(TypeError):
            input_redirection(args)

    def test_input_redirection_no_space_multiple_file_error(self):
        args = [
            "</comp0010/test/test_dir/test_dir1/test_file1.txt</comp0010/test/test_dir/test_dir1/test_file2.txt",
        ]
        with self.assertRaises(TypeError):
            input_redirection(args)

    def test_input_redirection_file_not_extists(self):
        args = ["<", "/comp0010/test/test_dir/test_dir1/test_nofile.txt"]
        with self.assertRaises(FileNotFoundError):
            input_redirection(args)

    def test_input_redirection_infront(self):
        expected = ("cat", ["dir1/file2.txt"])
        output = eval_cmd("< dir1/file2.txt cat")
        self.assertEqual(expected, output)

    def test_input_redirection_infront_no_space(self):
        expected = ("cat", ["dir1/file1.txt"])
        output = eval_cmd("<dir1/file1.txt cat")
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
