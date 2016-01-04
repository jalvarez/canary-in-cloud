import unittest
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
