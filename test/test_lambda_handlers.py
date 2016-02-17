from dynamodb_test import TwistedDynamoDbTestCase
from mock import Mock
from boto3.dynamodb.conditions import Key
from functools import partial

from src import _get_all_defers_listen_and_alert

class LambdaHandlersTests(TwistedDynamoDbTestCase):

    def setUp(self):
        super(LambdaHandlersTests, self).setUp()
        self.scan_result_table = self.dynamodb.Table('scan_result')

    def get_count_scan_result(self):
        return self.scan_result_table.scan(Select='COUNT')['Count']

    def _check_result_counters(self, previous_result_counter, dummy):
        print ">> Result counters: %d" % previous_result_counter
        result_counter = self.get_count_scan_result()
        self.assertGreater(result_counter, previous_result_counter)

    def test_scan_handler_insert_new_result(self):
        previous_result_counter = self.get_count_scan_result()
        _get_all_defers_listen_and_alert(partial(self._check_result_counters, \
                                                 previous_result_counter))
