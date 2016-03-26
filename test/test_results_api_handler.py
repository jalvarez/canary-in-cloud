from dynamodb_test import DynamoDbTestCase
from mock import Mock
import json

from src import AWSContext
from src import CanaryInCloudAPI

class ResultsApiHandlerTests(DynamoDbTestCase):
    def setUp(self):
        super(ResultsApiHandlerTests, self).setUp()
        self.FUNCTION_NAME = 'CanaryInCloudAPI_TEST'
        self.ctx = AWSContext(self.FUNCTION_NAME)
        self.api = CanaryInCloudAPI(self.ctx)

    def test_get_results_default_100_items(self):
        event = { 'client_id': 'test', \
                  'url_number': 1 }
        json_response = self.api.handler('results', event)
        results = json.loads(json_response)
        self.assertEquals(len(results), 100)

    def test_get_results_50_items(self):
        event = { 'client_id': 'test', \
                  'url_number': 1, \
                  'n_items': 50 }
        json_response = self.api.handler('results', event)
        results = json.loads(json_response)
        self.assertEquals(len(results), 50)

    def test_get_results_from_a_valid_date(self):
        a_valid_date = '2016-02-15T12:00:00.000000'
        event = { 'client_id': 'test', \
                  'url_number': 1, \
                  'from': a_valid_date }
        json_response = self.api.handler('results', event)
        results = json.loads(json_response)
        self.assertGreater(len(results), 0)
        self.assertGreater(results[0]['timestamp_iso'], a_valid_date)

