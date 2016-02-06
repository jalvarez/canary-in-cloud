import unittest
from mock import Mock

import src

class ListenerMinerTests(unittest.TestCase):
	def setUp(self):
		an_urls = [{ 'url': 'http://test.com' }]
		self.clients_repository_mock = Mock()
		self.clients_repository_mock.get_client_urls = Mock(return_value=an_urls)
		self.results_repository_mock = Mock()
		self.miners_factory = src.ListenerMinersFactory( \
												self.clients_repository_mock, \
												self.results_repository_mock)
	
	def config_results_serie(self, return_result):
		results_serie_mock = Mock()
		results_serie_mock.last_result = Mock(return_value=return_result)
		self.results_repository_mock.resultsSerie_by_url = Mock( \
												return_value=results_serie_mock)

	def test_not_ok_listener_alert(self):
		failed_result = { 'status_code': 500 }
		self.config_results_serie(failed_result)
		client_id = 'TEST'
		not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
														client_id)
		not_ok_listener_miner.listen()
		self.assertTrue(not_ok_listener_miner.is_alert())

