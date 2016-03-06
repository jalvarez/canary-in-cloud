from dynamodb_test import TwistedDynamoDbTestCase
import twisted.trial.unittest
from boto3.dynamodb.conditions import Key
from functools import partial

from src import _get_all_defers_listen_and_alert
from src import AWSContext

class ScanHandlerTests(TwistedDynamoDbTestCase):
    def setUp(self):
        super(ScanHandlerTests, self).setUp()
        self.scan_result_table = self.dynamodb.Table('scan_result')
        self.ctx = AWSContext('CanaryInCloudScan_TEST')

    def _get_url_to_test(self):
        clients = self.ctx.clients_repository.get_clients()
        a_client_id = clients[0]['client_id']
        urls = self.ctx.clients_repository.get_client_urls(a_client_id)
        a_url = urls[0]['url']
        return a_url

    def _get_count_scan_result(self, url):
        return self.ctx.results_repository.count_results_by_url(url)

    def _check_result_counters(self, url, previous_result_counter, dummy):
        result_counter = self._get_count_scan_result(url)
        self.assertGreater(result_counter, previous_result_counter)

    def test_scan_handler_insert_new_result(self):
        url = self._get_url_to_test()
        previous_result_counter = self._get_count_scan_result(url)
        return _get_all_defers_listen_and_alert(self.ctx, \
                                                 partial( \
                                                  self._check_result_counters,\
                                                  url, \
                                                  previous_result_counter))
