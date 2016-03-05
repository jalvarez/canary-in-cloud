from twisted.trial import unittest
from mock import Mock
from functools import partial
from twisted.internet import defer

import src

class AlertAlwaysListenerMiner(src.ListenerMiner):
    def __init__(self, clients_repository, results_repository, client_id):
        src.ListenerMiner.__init__(self, clients_repository, \
                                         results_repository, \
                                         client_id)
        self.message = src.Message('a message', 'oh oh')
        
    def alerter(self, url):
        self.alert(self.message)

    def listen(self, cage, callback):
        self.listen_canaries_and_alert(cage, \
                                       lambda x,_: True, \
                                       self.alerter, \
                                       callback)

    def get_message(self):
        return self.message

class SequenceListenerMiner(src.ListenerMiner):
    def listen(self, boolean_sequence, callback):
        self.listen_canaries_and_alert(boolean_sequence, \
                                       lambda x,_: x, \
                                       lambda y: None, \
                                       callback)
        
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
        self.miners_factory = src.ListenerMinersFactory( \
                                                self.clients_repository_mock, \
                                                self.results_repository_mock)
    
    def _config_results_serie(self, return_result):
        results_serie_mock = Mock()
        results_serie_mock.last_result = Mock(return_value=return_result)
        self.results_repository_mock.resultsSerie_by_url = Mock( \
                                                return_value=results_serie_mock)

    def _canary_ch_reg(self, return_result, callback):
        d = defer.Deferred()
        d.addCallback(partial(callback, return_result))
        return d

    def _config_canary(self, return_result):
        canary_mock = Mock()
        canary_mock.check_and_register = Mock(side_effect=
                                            partial(self._canary_ch_reg, \
                                                    return_result))
        return canary_mock

    def _check_channel_sendMessage_called(self, channel, listener):
        channel.sendMessage.assert_called_once_with( \
                                                listener_miner.get_message())

    def test_a_listener_in_alert_send_a_message_in_channel(self):
        a_channel = Mock()
        a_channel.sendMessage = Mock()
        self.clients_repository_mock.get_client_channels = Mock(\
                                                    return_value=[a_channel])

        cage = [Mock()]

        a_listener_miner = self.miners_factory.new(AlertAlwaysListenerMiner,\
                                                   self.CLIENT_ID)
        return a_listener_miner.listen(cage, \
                                       partial( \
                                        self._check_channel_sendMessage_called,\
                                        a_channel, \
                                        a_listener_miner))

    def _assert_with_listener(self, assert_method, \
                              listener, listener_func, expected=None):
        assert_method(listener_func(listener),expected)

    def test_not_ok_listener_alert(self):
        cage = [self._config_canary(self.FAILED_RESULT)]
        self._config_results_serie(self.OK_RESULT)

        not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
                                                        self.CLIENT_ID)
        return not_ok_listener_miner.listen(cage, \
                                             partial(
                                                self._assert_with_listener, \
                                                self.assertTrue, \
                                                not_ok_listener_miner,
                                                lambda _: _.is_alert()))

    def test_not_ok_listener_not_changes_not_alert(self):
        cage = [self._config_canary(self.FAILED_RESULT)]
        self._config_results_serie(self.FAILED_RESULT)
        not_ok_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
                                                        self.CLIENT_ID)
        return not_ok_listener_miner.listen(cage, \
                                              partial(
                                                self._assert_with_listener, \
                                                self.assertFalse, \
                                                not_ok_listener_miner,
                                                lambda _: _.is_alert()))

    def test_a_listener_is_alert_when_at_least_a_url_fail(self):
        cage = [self._config_canary(self.FAILED_RESULT),
                self._config_canary(self.OK_RESULT)]
        self._config_results_serie(self.OK_RESULT)
        a_listener_miner = self.miners_factory.new(src.NotOkListenerMiner,\
                                                   self.CLIENT_ID)
        return a_listener_miner.listen(cage, \
                                        partial(self._assert_with_listener, \
                                               self.assertTrue, \
                                               a_listener_miner,
                                               lambda _: _.is_alert()))
        
    def test_recovery_listener(self):
        cage = [self._config_canary(self.OK_RESULT)]
        self._config_results_serie(self.FAILED_RESULT)
        recovery_listener_miner = self.miners_factory.new( \
                                                    src.RecoveryListenerMiner,\
                                                    self.CLIENT_ID)
        return recovery_listener_miner.listen(cage, \
                                              partial(\
                                                   self._assert_with_listener, \
                                                   self.assertTrue, \
                                                   recovery_listener_miner,
                                                   lambda _: _.is_alert()))
        
    def test_recovery_listener_with_no_changes(self):
        cage = [self._config_canary(self.FAILED_RESULT)]
        self._config_results_serie(self.FAILED_RESULT)
        recovery_listener_miner = self.miners_factory.new( \
                                                    src.RecoveryListenerMiner,\
                                                    self.CLIENT_ID)
        return recovery_listener_miner.listen(cage, \
                                              partial(\
                                                self._assert_with_listener, \
                                                self.assertFalse, \
                                                recovery_listener_miner,
                                                lambda _: _.is_alert()))

    def test_last_result_listener_is_nok_without_results(self):
        cage = [self._config_canary(self.FAILED_RESULT)]
        self._config_results_serie(None)
        last_result_listener_miner = self.miners_factory.new( \
                                                   src.LastResultListenerMiner,\
                                                   self.CLIENT_ID)
        last_result = last_result_listener_miner.get_last_result('a url')
        self.assertFalse(last_result_listener_miner.is_result_ok(last_result))
