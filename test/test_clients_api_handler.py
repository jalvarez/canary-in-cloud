from dynamodb_test import DynamoDbTestCase
from mock import Mock
import json

from src import AWSContext
from src import clients_api_handler
from src import client_url_api_handler

class ClientsApiHandlerTests(DynamoDbTestCase):
    def setUp(self):
        super(ClientsApiHandlerTests, self).setUp()
        self.FUNCTION_NAME = 'CanaryInCloudAPI_TEST'
        self.ctx = AWSContext(self.FUNCTION_NAME)
        self._create_context_mock(self.FUNCTION_NAME)

    def _create_context_mock(self, function_name):
        self.context_mock = Mock()
        self.context_mock.function_name = function_name

    def test_get_clients(self):
        event = None
        json_response = clients_api_handler(event, self.context_mock)
        clients = json.loads(json_response)
        self.assertGreater(len(clients), 0)
        client = clients[0]
        self.assertIsNotNone(client['client_id'])

    def test_get_client_url(self):
        event = { 'client_id': 'test' }
        json_response = client_url_api_handler(event, self.context_mock)
        urls = json.loads(json_response)
        self.assertGreater(len(urls), 0)
        url = urls[0]
        self.assertIsNotNone(url['url'])
