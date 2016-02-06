import unittest
from mock import Mock
import boto3
import logging

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

	def check_and_register(self, url):
		canary = src.Canary(self.result_table, url)
		check = canary.check()
		canary.register_response()
		return check

	def test_last_result_after_check_and_register(self):
		url = 'http://www.google.com'
		check_result = self.check_and_register(url)
		rs = self.results_repository.resultsSerie_by_url(url)
		result = rs.last_result()
		self.assertEquals(	check_result['code'], 
							result['status_code'])
		self.assertEquals(	check_result['timestamp_iso'], 
							result['timestamp_iso'])
