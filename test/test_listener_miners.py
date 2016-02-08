import unittest
from mock import Mock

import src

class AlertAlwaysListenerMiner(src.ListenerMiner):
	def __init__(self, 	clients_repository, results_repository, \
						canary_factory, client_id):
		src.ListenerMiner.__init__(self, clients_repository, \
										 results_repository, \
										 canary_factory, \
										 client_id)
		self.message = src.Message('a message', 'oh oh')
		
	def alerter(self, url):
		self.alert(self.message)

	def listen(self):
		self.listen_urls_and_alert(lambda x,_: True, self.alerter)

	def get_message(self):
		return self.message

class SequenceListenerMiner(src.ListenerMiner):
	def set_listen_sequence_results(self, results_sequence):
		self.results_sequence = results_sequence

	def get_urls(self):
		return self.results_sequence

	def listen(self):
		self.listen_urls_and_alert(lambda x,_: x, lambda y: None)
		
class ListenerMinerTests(unittest.TestCase):
	def setUp(self):
		an_urls = [{ 'url': 'http://test.com' }]
		self.CLIENT_ID = 'TEST'
		self.FAILED_RESULT = { 'status_code': 500 }
		self.OK_RESULT = { 'status_code': 200 }

		self.clients_repository_mock = Mock()
		self.clients_repository_mock.get_client_urls = Mock(return_value=an_urls)
		self.clients_repository_mock.get_client_channels = Mock(return_value=[])
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

	def test_a_listener_in_alert_send_a_message_in_channel(self):
		a_channel = Mock()
		a_channel.sendMessage = Mock()
		self.clients_repository_mock.get_client_channels = Mock(\
													return_value=[a_channel])
		
		a_listener_miner = self.miners_factory.new(AlertAlwaysListenerMiner,\
												   self.CLIENT_ID)
		a_listener_miner.listen()
		a_channel.sendMessage.assert_called_once_with( \
												a_listener_miner.get_message())

	def test_not_ok_listener_alert(self):
		self.config_canary(self.FAILED_RESULT)
		self.config_results_serie(self.OK_RESULT)
		not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
														self.CLIENT_ID)
		not_ok_listener_miner.listen()
		self.assertTrue(not_ok_listener_miner.is_alert())

	def test_not_ok_listener_not_changes_not_alert(self):
		self.config_canary(self.FAILED_RESULT)
		self.config_results_serie(self.FAILED_RESULT)
		not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
														self.CLIENT_ID)
		not_ok_listener_miner.listen()
		self.assertFalse(not_ok_listener_miner.is_alert())

	def test_a_listener_is_alert_when_at_least_a_url_fail(self):
		a_listener_miner = self.miners_factory.new(SequenceListenerMiner,\
												   self.CLIENT_ID)
		a_listener_miner.set_listen_sequence_results([False, True])
		a_listener_miner.listen()
		self.assertTrue(a_listener_miner.is_alert())
		
	def test_recovery_listener(self):
		self.config_canary(self.OK_RESULT)
		self.config_results_serie(self.FAILED_RESULT)
		recovery_listener_miner = self.miners_factory.new( \
													src.RecoveryListenerMiner,\
													self.CLIENT_ID)
		recovery_listener_miner.listen()
		self.assertTrue(recovery_listener_miner.is_alert())
		
	def test_recovery_listener_with_no_changes(self):
		self.config_canary(self.FAILED_RESULT)
		self.config_results_serie(self.FAILED_RESULT)
		recovery_listener_miner = self.miners_factory.new( \
													src.RecoveryListenerMiner,\
													self.CLIENT_ID)
		recovery_listener_miner.listen()
		self.assertFalse(recovery_listener_miner.is_alert())

