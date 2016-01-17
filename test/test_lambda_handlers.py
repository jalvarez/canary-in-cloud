from dynamodb_test import DynamoDbTestCase
from mock import Mock
from boto3.dynamodb.conditions import Key

from src import scan_handler

class LambdaHandlersTests(DynamoDbTestCase):

	def setUp(self):
		super(LambdaHandlersTests, self).setUp()
		self.scan_result_table = self.dynamodb.Table('scan_result')

	def get_count_scan_result(self):
		return self.scan_result_table.scan(Select='COUNT')['Count']

	def test_scan_handler_insert_new_result(self):
		event_mock = Mock()
		context_handler_mock = Mock()
		previous_result_counter = self.get_count_scan_result()
		scan_handler(event_mock, context_handler_mock)
		result_counter = self.get_count_scan_result()
		self.assertGreater(result_counter, previous_result_counter)
