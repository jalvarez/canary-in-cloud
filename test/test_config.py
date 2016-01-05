import unittest
from mock import Mock
import boto3
import types
import logging

import src

class ConfigTests(unittest.TestCase):
	def setUp(self):
		boto3.set_stream_logger('botocore', logging.WARNING)
		dynamodb = boto3.resource('dynamodb')
		self.config_table = dynamodb.Table('config')

	def test_config_contains_smtp_port(self):
		config = src.Config(self.config_table, 'TEST')
		self.assertIsNotNone(config.get('SMTP_PORT'))

	def test_config_smtp_port_is_number(self):
		config = src.Config(self.config_table, 'TEST')
		self.assertEquals(type(config.get('SMTP_PORT')), types.IntType)
