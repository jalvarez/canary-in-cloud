import unittest
from src import canary

class CanaryTests(unittest.TestCase):

	def test_wrong_url(self):
		result = canary.check_url('http://estaurlseguroquenoexiste.com')
		self.assertEqual(404, result['code'])

	def test_ok_url(self):
		result = canary.check_url('http://www.google.com')
		self.assertEqual(200, result['code'])

	def test_ok_timing_measured(self):
		result = canary.check_url('http://www.google.com')
		self.assertGreater(result['time'], 0)
