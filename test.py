# coding=utf-8
import os
import tempfile
import unittest

from copy_utils import fast_copy, get_path, default_copy, copy_copy


class CopyTestCases(unittest.TestCase):
    def test_fast_copy_with_long_name(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        long_path = os.path.abspath(("б" * 64 + os.sep) * 30)
        dest = os.path.join(long_path, os.path.basename(temp_file.name))
        try:
            fast_copy(temp_file.name, dest)
            self.assertTrue(os.path.exists(get_path(dest)))
        finally:
            os.remove(get_path(dest))
            os.removedirs(get_path(os.path.dirname(dest)))

    def test_default_copy_with_long_name(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        long_path = os.path.abspath(("a" * 128 + os.sep) * 30)
        dest = os.path.join(long_path, os.path.basename(temp_file.name))
        try:
            default_copy(temp_file.name, dest)
            default_copy(temp_file.name, dest)
            self.assertTrue(os.path.exists(get_path(dest)))
        finally:
            os.remove(get_path(dest))
            os.removedirs(get_path(os.path.dirname(dest)))

    def test_copy_copy_with_long_name(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        long_path = os.path.abspath(("a" * 128 + os.sep) * 30)
        dest = os.path.join(long_path, os.path.basename(temp_file.name))
        try:
            copy_copy(temp_file.name, dest)
            self.assertTrue(os.path.exists(get_path(dest)))
        finally:
            os.remove(get_path(dest))
            os.removedirs(get_path(os.path.dirname(dest)))


if __name__ == '__main__':
    unittest.main()
