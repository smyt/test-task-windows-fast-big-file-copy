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

    def test_fast_copy_with_long_name_1(self):
        src_path = "C:\\Users\\Public\\Documents\\00000000000000000000000000000000000000000000000000\\11111111111111111111111111111111111111111111111111\\22222222222222222222222222222222222222222222222222\\33333333333333333333333333333333333333333333333333\\44444444444444444444444444444444444444444444444444\\55555555555555555555555555555555555555555555555555\\66666666666666666666666666666666666666666666666666\\777777777777777777777777777777777777777777777777777\\88888888888888888888888888888888888888888888888888\\99999999999999999999999999999999999999999999999999\\00000000000000000000000000000000000000000000000000\\тест1\\file.txt"
        with open(get_path(src_path), 'w'):
            pass

        try:
            fast_copy(
                src_path,
                'C:\\Users\\Public\\Documents\\00000000000000000000000000000000000000000000000000\\11111111111111111111111111111111111111111111111111\\22222222222222222222222222222222222222222222222222\\33333333333333333333333333333333333333333333333333\\44444444444444444444444444444444444444444444444444\\55555555555555555555555555555555555555555555555555\\66666666666666666666666666666666666666666666666666\\777777777777777777777777777777777777777777777777777\\88888888888888888888888888888888888888888888888888\\99999999999999999999999999999999999999999999999999\\тест1\\file2.txt'
            )
        finally:
            os.remove(get_path(src_path))

        src_path = u'C:\\Users\\Public\\Documents\\качество\\0.txt'
        with open(src_path, 'w'):
            pass

        try:
            fast_copy(src_path, 'C:\\Users\\Public\\Documents\\1.txt')
            fast_copy(u'C:\\Users\\Public\\Documents\\качество\\0.txt', u'C:\\Users\\Public\\Documents\\1.txt')
        finally:
            os.remove(get_path(src_path))


if __name__ == '__main__':
    unittest.main()
