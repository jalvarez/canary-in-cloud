import unittest
from mock import Mock
import boto3
import logging

import src

class SmtpDispatcherTests(unittest.TestCase):
	def setUp(self):
		boto3.set_stream_logger('botocore', logging.WARNING)
		dynamodb = boto3.resource('dynamodb')
		config_table = dynamodb.Table('config')
		self.config = src.Config(config_table, 'TEST')

	def test_send_email(self):
		smtp_dispatcher = src.SmtpDispatcher(self.config)
		smtp_dispatcher.send('juanmi.alvarez@gmail.com', 
							'Test email',
							'It is a test.')
