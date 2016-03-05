from twisted.trial import unittest
import types
from functools import partial
from mock import Mock
from twisted.internet import reactor
from twisted.web.client import Agent

import src

class CanaryTests(unittest.TestCase):
    def setUp(self):
        self.result_table_mock = Mock()

    def _create_new_canary(self, url):
        return src.Canary(self.result_table_mock, Agent(reactor), url)

    def _check_callback(self, assert_method, result_func, expected, result):
        assert_method(result_func(result), expected)

    def _in_canary_check(self, canary, \
                        assert_method, result_func, expected=None):
        return canary.check(partial(self._check_callback, \
                             assert_method, result_func, expected))

    def test_wrong_url(self):
        canary = self._create_new_canary('https://estaurlseguroquenoexiste.com')
        return self._in_canary_check(canary, \
                                  self.assertEqual, lambda x: x['status_code'],\
                                  404)

    def test_ok_url(self):
        canary = self._create_new_canary('https://www.google.com')
        return self._in_canary_check(canary, \
                                    self.assertIn, lambda x: x['status_code'],\
                                    [200, 302])

    def test_ok_duration_measured(self):
        canary = self._create_new_canary('https://www.google.com')
        return self._in_canary_check(canary, \
                                self.assertGreater, lambda x: x['duration'], 0)

    def test_ok_with_timestamp(self):
        canary = self._create_new_canary('https://www.google.com')
        return self._in_canary_check(canary, \
                                self.assertIsNotNone, lambda x: x['timestamp'])

    def test_timestamp_is_string(self):
        canary = self._create_new_canary('https://www.google.com')
        return self._in_canary_check(canary, \
                                self.assertIn, lambda x: type(x['timestamp']), \
                                types.StringTypes)

    def test_duration_is_integer(self):
        canary = self._create_new_canary('https://www.google.com')
        return self._in_canary_check(canary, \
                            self.assertEquals, lambda x: type(x['duration']), \
                            types.IntType)

    def test_not_register_without_check(self):
        canary = self._create_new_canary('https://www.google.com')
        self.assertRaises(src.RegisterWithoutCheckError, \
                          canary.register_response)

    def _check_other_callback(self, other_callback, check_result):
        self.assertEquals(len(other_callback.mock_calls), 1)

    def test_check_with_double_callback(self):
        canary = self._create_new_canary('https://www.google.com')
        callback_1 = Mock()
        request = canary.check(callback_1)
        return canary.check(partial(self._check_other_callback, callback_1))

    def test_dont_response_url(self):
        canary = self._create_new_canary('http://www.google.com:81')
        return self._in_canary_check(canary, \
                                  self.assertEqual, lambda x: x['status_code'],\
                                  418)
