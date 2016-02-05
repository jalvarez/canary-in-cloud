import unittest
from dynamodb_test import DynamoDbTestCase
import src

class ClientsRepositoryTests(DynamoDbTestCase):

	def setUp(self):
		super(ClientsRepositoryTests, self).setUp()
		self.TEST_CLIENT_ID = 'test'
		self.clients_table = self.dynamodb.Table('clients')
		self.url2scan_table = self.dynamodb.Table('url2scan')
		config = src.Config(self.dynamodb.Table('config'), 'TEST')

		self.repository = src.ClientsRepository(self.clients_table, self.url2scan_table, config)

	def test_get_client(self):
		client = self.repository.get_client(self.TEST_CLIENT_ID)
		self.assertIsNotNone(client)
		self.assertEqual(client['client_id'], self.TEST_CLIENT_ID)
		
	def test_get_client_urls(self):
		urls = self.repository.get_client_urls(self.TEST_CLIENT_ID)
		self.assertIsNotNone(urls)
		self.assertGreater(len(urls), 0)
		first_url = urls[0]
		self.assertIsNotNone(first_url['url'])
		self.assertEqual(first_url['url'][:4], 'http')

	def test_get_clients(self):
		clients = self.repository.get_clients()
		self.assertIsNotNone(clients)
		self.assertGreater(len(clients), 0)

	def test_get_client_channels(self):
		channels = self.repository.get_client_channels(self.TEST_CLIENT_ID)
		self.assertIsNotNone(channels)
		self.assertTrue(isinstance(channels[0], src.Channel))
