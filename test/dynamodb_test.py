import unittest
import twisted.trial.unittest
import boto3
import logging

class DynamoDbAccess:
	def get_resource(self):
		boto3.set_stream_logger('botocore', logging.WARNING)
		boto3.set_stream_logger('boto3.resources', logging.WARNING)
		return boto3.resource('dynamodb')

class DynamoDbTestCase(unittest.TestCase):
	def setUp(self):
		self.dynamodb = DynamoDbAccess().get_resource()

class TwistedDynamoDbTestCase(twisted.trial.unittest.TestCase):
	def setUp(self):
		self.dynamodb = DynamoDbAccess().get_resource()
