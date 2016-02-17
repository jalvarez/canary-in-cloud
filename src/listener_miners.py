import logging
from functools import partial

from channel_factory import Message

class ListenerMiner:
    def __init__(self,  clients_repository, results_repository, \
                        canary_factory, client_id):
        self.clients_repository = clients_repository
        self.results_repository = results_repository
        self.canary_factory = canary_factory
        self.client_id = client_id
        self._is_alert = False

    def _check_listener_result(self, listener, url, result):
        listener_result = listener(url, result)
        self._is_alert = self._is_alert or listener_result

    def listen_url(self, url, listener):
        canary = self.canary_factory.new(url)
        return canary.check_and_register(partial(self._check_listener_result, \
                                                 listener, \
                                                 url))

    def _alert_callback(self, url, alerter, callback, dummy):
        if (self._is_alert):
            alerter(url)
        callback()
        
    def listen_and_alert_url(self, url, listener, alerter, callback):
        listen_result = self.listen_url(url, listener)
        listen_result.addCallback(partial(self._alert_callback, \
                                          url, \
                                          alerter, \
                                          callback))
        return listen_result

    def get_urls(self):
        return map(lambda x: x['url'], \
                    self.clients_repository.get_client_urls(self.client_id))

    def listen_urls_and_alert(self, listener, alerter, callback):
        return map(lambda url: self.listen_and_alert_url(url, \
                                                         listener, \
                                                         alerter, \
                                                         callback),
                    self.get_urls())

    def is_alert(self):
        return self._is_alert
    
    def alert(self, message):
        channels = self.clients_repository.get_client_channels(self.client_id)
        for channel in channels:
            channel.sendMessage(message)

class LastResultListenerMiner(ListenerMiner):
    def is_result_ok(self, result):
        return (result['status_code'] == 200)

    def get_last_result(self, url):
        results_serie = self.results_repository.resultsSerie_by_url(url)
        return results_serie.last_result()

    def listen(self):
        raise 'Not implemented'

class NotOkListenerMiner(LastResultListenerMiner):
    def not_ok_listener(self, url, canary_check):
        last_result = self.get_last_result(url)
        return self.is_result_ok(last_result) and \
                not self.is_result_ok(canary_check)

    def not_ok_alerter(self, url):
        self.alert(Message("%s is down" % url, \
                           ("Dear user,\n%s has been detected as DOWN.\n"+
                            "Regards.\nCanary In Cloud") % url))

    def listen(self, callback):
        return self.listen_urls_and_alert(self.not_ok_listener, \
                                          self.not_ok_alerter, \
                                          callback)
    
class RecoveryListenerMiner(LastResultListenerMiner):
    def recovery_listener(self, url, canary_check):
        last_result = self.get_last_result(url)
        return not self.is_result_ok(last_result) and \
                self.is_result_ok(canary_check)

    def recovery_alerter(self, url):
        self.alert(Message("%s is up" % url, \
                           ("Dear user,\n%s has been detected as UP.\n"+
                            "Regards.\nCanary In Cloud") % url))

    def listen(self, callback):
        self.listen_urls_and_alert(self.recovery_listener, \
                                   self.recovery_alerter, \
                                   callback)

class ListenerMinerTeam:
    def __init__(self):
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def listen(self):
        for member in self.members:
            try:
                member.listen()
            except Exception as e:
                logging.exception("Listener miner failed: %s" % \
                                    self.__class__.__name__)

class ListenerMinersFactory:
    def __init__(self, clients_repository, results_repository, canary_factory):
        self.clients_repository = clients_repository
        self.results_repository = results_repository
        self.canary_factory = canary_factory

    def new(self, minerClass, client_id):
        return minerClass(self.clients_repository, \
                          self.results_repository, \
                          self.canary_factory, \
                          client_id)
