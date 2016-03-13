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
        self.assertGreater(len(results), 0)
