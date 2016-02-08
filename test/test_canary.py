import unittest
import types
from mock import Mock

import src

class CheckUrlTests(unittest.TestCase):
	def setUp(self):
		self.result_table_mock = Mock()

	def aNewCanary(self, url):
		return src.Canary(self.result_table_mock, url)

	def test_wrong_url(self):
		canary = self.aNewCanary('http://estaurlseguroquenoexiste.com')
		result = canary.check()
		self.assertEqual(404, result['status_code'])

	def test_ok_url(self):
		canary = self.aNewCanary('http://www.google.com')
		result = canary.check()
		self.assertEqual(200, result['status_code'])

	def test_ok_duration_measured(self):
		canary = self.aNewCanary('http://www.google.com')
		result = canary.check()
		self.assertGreater(result['duration'], 0)

	def test_ok_with_timestamp(self):
		canary = self.aNewCanary('http://www.google.com')
		result = canary.check()
		self.assertIsNotNone(result['timestamp'])

	def test_timestamp_is_string(self):
		canary = self.aNewCanary('http://www.google.com')
		result = canary.check()
		timestamp = result['timestamp']
		self.assertIn(type(timestamp), types.StringTypes)

	def test_duration_is_integer(self):
		canary = self.aNewCanary('http://www.google.com')
		result = canary.check()
		duration = result['duration']
		self.assertEquals(type(duration), types.IntType)

	def test_not_register_without_check(self):
		canary = self.aNewCanary('http://www.google.com')
		self.assertRaises(src.RegisterWithoutCheckError, canary.register_response)
