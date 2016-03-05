from twisted.trial import unittest
from mock import Mock
import boto3
import logging
from functools import partial
from twisted.internet import reactor
from twisted.web.client import Agent

import src

class ResultsRepositoryTests(unittest.TestCase):
    def setUp(self):
        boto3.set_stream_logger('botocore', logging.WARNING)
        dynamodb = boto3.resource('dynamodb')
        self.result_table = dynamodb.Table('scan_result')
        self.results_repository = src.ResultsRepository(self.result_table)

    def test_last_result_empty(self):
        url = 'http://estaurlseguroquenoexiste.com'
        rs = self.results_repository.resultsSerie_by_url(url)
        self.assertIsNone(rs.last_result())

    def _get_defer_check_result(self, url):
        canary = src.Canary(self.result_table, Agent(reactor), url)
        return canary.check_and_register(lambda _: _)

    def _callback_get_resultsSerie(self, url, check_result):
        rs = self.results_repository.resultsSerie_by_url(url)
        result = rs.last_result()
        return (result, check_result)

    def _assert_equals(self, attribute, params):
        (check_result, result) = params
        self.assertEquals(check_result[attribute], result[attribute])
        return (check_result, result)

    def test_last_result_after_check_and_register(self):
        url = 'http://www.google.com'
        defer = self._get_defer_check_result(url)
        defer.addCallback(partial(self._callback_get_resultsSerie, url))
        defer.addCallback(partial(self._assert_equals, 'status_code'))
        defer.addCallback(partial(self._assert_equals, 'timestamp_iso'))
        return defer

    def _check_count_results(self, url, previous_count, dummy):
        after_count = self.results_repository.count_results_by_url(url)
        self.assertGreater(after_count, previous_count)

    def test_count_result_after_check_and_register(self):
        url = 'http://www.google.com'
        previous_count = self.results_repository.count_results_by_url(url)
        defer = self._get_defer_check_result(url)
        defer.addCallback(partial(self._check_count_results, url, previous_count))
        return defer
        
