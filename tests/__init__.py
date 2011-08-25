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

    def test_ignore_url(self):
        """Test ignore setup"""
        ok_(True == inliner.ignore_url('http://domain.com/google-analyticator/tracking.min.js'),
                    "the url should be ignored due to blacklist")
        ok_(False == inliner.ignore_url('http://google.com/'),
                    "the url should NOT be ignored due to blacklist")
        ok_(True == inliner.ignore_url('http://s3.amazonaws.com/getsatisfaction.com/javascripts/feedback-v2.js'),
                    "the url should be ignored due to blacklist")

    def test_get_content_local(self):
        """Test that we can get a local content"""
        TEST_PATH = "tests/sample/local.html"
        TEST_CONTENT = "Local Test"

        con = inliner.get_content(TEST_PATH)

        ok_(TEST_CONTENT in con,
                "Should find {0} in the test content: {1}".format(
                    TEST_CONTENT,
                    con))

    def test_get_content_remote(self):
        """Test that we can get a remove content"""
        TEST_PATH = "http://google.com"
        TEST_CONTENT = "Feeling Lucky"

        con = inliner.get_content(TEST_PATH)

        ok_(TEST_CONTENT in con,
                "Should find {0} in the test content: {1}".format(
                    TEST_CONTENT,
                    con))
