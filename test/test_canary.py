import unittest
import types
from decimal import Decimal

import src

class CheckUrlTests(unittest.TestCase):

	def test_wrong_url(self):
		canary = src.Canary('http://estaurlseguroquenoexiste.com')
		result = canary.check()
		self.assertEqual(404, result['code'])

	def test_ok_url(self):
		canary = src.Canary('http://www.google.com')
		result = canary.check()
		self.assertEqual(200, result['code'])

	def test_ok_duration_measured(self):
		canary = src.Canary('http://www.google.com')
		result = canary.check()
		self.assertGreater(result['duration'], 0)

	def test_ok_with_timestamp(self):
		canary = src.Canary('http://www.google.com')
		result = canary.check()
		self.assertIsNotNone(result['timestamp'])

	def test_timestamp_is_string(self):
		canary = src.Canary('http://www.google.com')
		result = canary.check()
		timestamp = result['timestamp']
		self.assertIn(type(timestamp), types.StringTypes)

	def test_duration_is_integer(self):
		canary = src.Canary('http://www.google.com')
		result = canary.check()
		duration = result['duration']
		self.assertEquals(type(duration), types.IntType)
