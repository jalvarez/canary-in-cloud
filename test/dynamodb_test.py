import unittest
import boto3
import logging

class DynamoDbTestCase(unittest.TestCase):
		
	def setUp(self):
		boto3.set_stream_logger('botocore', logging.WARNING)
		boto3.set_stream_logger('boto3.resources', logging.WARNING)
		self.dynamodb = boto3.resource('dynamodb')
