"""Tests for the inliner source"""
from nose.tools import ok_
from unittest import TestCase

from pythonwebpageinliner import inliner

class TestHelpers(TestCase):
    """Testing the helper functions we build the inliner from"""

    def setUp(self):
        """Setup Tests"""
        pass

    def tearDown(self):
        """Tear down each test"""
        pass

    def test_is_remote(self):
        """Verify that a url is a remote url"""

        tests = [
                (True, 'http://google.com'),
                (False, 'index.html'),
                (True, 'https://google.com'),
        ]

        for tst_case in tests:
            ok_(tst_case[0] == inliner.is_remote(tst_case[1]),
                    "The url failed to check is_remote: " + tst_case[1])
