import unittest

from dynamodb_test import DynamoDbTestCase

import src

class SmtpDispatcherTests(DynamoDbTestCase):
	def setUp(self):
		super(SmtpDispatcherTests, self).setUp()
		config_table = self.dynamodb.Table('config')
		self.config = src.Config(config_table, 'TEST')

	def test_send_email(self):
		smtp_dispatcher = src.SmtpDispatcher(self.config)
		smtp_dispatcher.send('juanmi.alvarez@gmail.com', 
							'Test email',
							'It is a test.')
