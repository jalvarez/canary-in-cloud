import unittest
from mock import Mock
import boto3
import logging

import src

class ResultsSerieTests(unittest.TestCase):
	def setUp(self):
		boto3.set_stream_logger('botocore', logging.WARNING)
		self.dynamodb = boto3.resource('dynamodb')
		self.result_table = self.dynamodb.Table('scan_result')

	def test_last_result_empty(self):
		rs = src.ResultsSerie(	'http://estaurlseguroquenoexiste.com', 
								self.result_table)
		self.assertIsNone(rs.last_result())

	def check_and_register(self, url):
		canary = src.Canary(url)
		check = canary.check()
		canary.register_response(self.result_table)
		return check

	def test_last_result_after_check_and_register(self):
		url = 'http://www.google.com'
		check_result = self.check_and_register(url)
		rs = src.ResultsSerie(url, self.result_table)
		result = rs.last_result()
		self.assertEquals(	check_result['code'], 
							result['status_code'])
		self.assertEquals(	check_result['timestamp_iso'], 
							result['timestamp_iso'])
