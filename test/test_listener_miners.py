import unittest
from mock import Mock

import src

class ListenerMinerTests(unittest.TestCase):
	def setUp(self):
		an_urls = [{ 'url': 'http://test.com' }]
		self.client_id = 'TEST'
		self.FAILED_RESULT = { 'status_code': 500 }
		self.OK_RESULT = { 'status_code': 200 }

		self.clients_repository_mock = Mock()
		self.clients_repository_mock.get_client_urls = Mock(return_value=an_urls)
		self.results_repository_mock = Mock()
		self.canary_factory_mock = Mock()
		self.miners_factory = src.ListenerMinersFactory( \
												self.clients_repository_mock, \
												self.results_repository_mock, \
												self.canary_factory_mock)
	
	def config_results_serie(self, return_result):
		results_serie_mock = Mock()
		results_serie_mock.last_result = Mock(return_value=return_result)
		self.results_repository_mock.resultsSerie_by_url = Mock( \
												return_value=results_serie_mock)

	def config_canary(self, return_result):
		canary_mock = Mock()
		canary_mock.check = Mock(return_value=return_result)
		self.canary_factory_mock.new = Mock(return_value=canary_mock)

	def test_not_ok_listener_alert(self):
		self.config_canary(self.FAILED_RESULT)
		self.config_results_serie(self.OK_RESULT)
		not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
														self.client_id)
		not_ok_listener_miner.listen()
		self.assertTrue(not_ok_listener_miner.is_alert())

	def test_not_ok_listener_not_changes_not_alert(self):
		self.config_canary(self.FAILED_RESULT)
		self.config_results_serie(self.FAILED_RESULT)
		not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
														self.client_id)
		not_ok_listener_miner.listen()
		self.assertFalse(not_ok_listener_miner.is_alert())
