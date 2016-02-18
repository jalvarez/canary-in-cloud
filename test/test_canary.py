from twisted.trial import unittest
import types
from functools import partial
from mock import Mock
from twisted.internet import reactor
from twisted.web.client import Agent

import src

class CheckUrlTests(unittest.TestCase):
    def setUp(self):
        self.result_table_mock = Mock()

    def aNewCanary(self, url):
        return src.Canary(self.result_table_mock, Agent(reactor), url)

    def check_callback(self, assert_method, result_func, expected, result):
        assert_method(result_func(result), expected)

    def in_canary_check(self, canary, \
                        assert_method, result_func, expected=None):
        return canary.check(partial(self.check_callback, \
                             assert_method, result_func, expected))

    def test_wrong_url(self):
        canary = self.aNewCanary('https://estaurlseguroquenoexiste.com')
        return self.in_canary_check(canary, \
                                  self.assertEqual, lambda x: x['status_code'],\
                                  404)

    def test_ok_url(self):
        canary = self.aNewCanary('https://www.google.com')
        return self.in_canary_check(canary, \
                                    self.assertIn, lambda x: x['status_code'],\
                                    [200, 302])

    def test_ok_duration_measured(self):
        canary = self.aNewCanary('https://www.google.com')
        return self.in_canary_check(canary, \
                                self.assertGreater, lambda x: x['duration'], 0)

    def test_ok_with_timestamp(self):
        canary = self.aNewCanary('https://www.google.com')
        return self.in_canary_check(canary, \
                                self.assertIsNotNone, lambda x: x['timestamp'])

    def test_timestamp_is_string(self):
        canary = self.aNewCanary('https://www.google.com')
        return self.in_canary_check(canary, \
                                self.assertIn, lambda x: type(x['timestamp']), \
                                types.StringTypes)

    def test_duration_is_integer(self):
        canary = self.aNewCanary('https://www.google.com')
        return self.in_canary_check(canary, \
                            self.assertEquals, lambda x: type(x['duration']), \
                            types.IntType)

    def test_not_register_without_check(self):
        canary = self.aNewCanary('https://www.google.com')
        self.assertRaises(src.RegisterWithoutCheckError, \
                          canary.register_response)
