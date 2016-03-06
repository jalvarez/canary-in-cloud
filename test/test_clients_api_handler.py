from dynamodb_test import DynamoDbTestCase
from mock import Mock
import json

from src import AWSContext
from src import CanaryInCloudAPI

class ClientsApiHandlerTests(DynamoDbTestCase):
    def setUp(self):
        super(ClientsApiHandlerTests, self).setUp()
        self.FUNCTION_NAME = 'CanaryInCloudAPI_TEST'
        self.ctx = AWSContext(self.FUNCTION_NAME)
        self.api = CanaryInCloudAPI(self.ctx)

    def test_get_clients(self):
        event = None
        json_response = self.api.handler('clients', event)
        clients = json.loads(json_response)
        self.assertGreater(len(clients), 0)
        client = clients[0]
        self.assertIsNotNone(client['client_id'])

    def test_get_client_url(self):
        event = { 'client_id': 'test' }
        json_response = self.api.handler('client_urls', event)
        urls = json.loads(json_response)
        self.assertGreater(len(urls), 0)
        url = urls[0]
        self.assertIsNotNone(url['url'])
