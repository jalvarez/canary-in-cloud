import logging
from functools import partial

from channel_factory import Message

class ListenerMiner:
    def __init__(self, clients_repository, results_repository, client_id):
        self.clients_repository = clients_repository
        self.results_repository = results_repository
        self.client_id = client_id
        self._is_alert = False

    def _check_listener_result(self, listener, check_result):
        url = check_result['url']
        listener_result = listener(url, check_result)
        self._is_alert = self._is_alert or listener_result
        return check_result

    def listen_canary(self, canary, listener):
        return canary.check_and_register(partial(self._check_listener_result, \
                                                 listener))

    def _alert_callback(self, alerter, callback, check_result):
        url = check_result['url']
        if (self._is_alert):
            alerter(url)
        callback(check_result)
        return check_result
        
    def listen_canary_and_alert(self, canary, listener, alerter, callback):
        listen_result = self.listen_canary(canary, listener)
        listen_result.addCallback(partial(self._alert_callback, \
                                          alerter, \
                                          callback))
        return listen_result

    def listen_canaries_and_alert(self, cage, listener, alerter, callback):
        return map(lambda canary: self.listen_canary_and_alert(canary, \
                                                               listener, \
                                                               alerter, \
                                                               callback),
                   cage)

    def is_alert(self):
        return self._is_alert
    
    def alert(self, message):
        channels = self.clients_repository.get_client_channels(self.client_id)
        for channel in channels:
            channel.sendMessage(message)

class LastResultListenerMiner(ListenerMiner):
    def is_result_ok(self, result):
        return (result and result['status_code'] == 200)

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

    def listen(self, cage, callback):
        return self.listen_canaries_and_alert(cage, \
                                              self.not_ok_listener, \
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

    def listen(self, cage, callback):
        return self.listen_canaries_and_alert(cage, \
                                              self.recovery_listener, \
                                              self.recovery_alerter, \
                                              callback)

class ListenerMinerTeam:
    def __init__(self):
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def listen(self, cage, callback):
        defers = []
        for member in self.members:
            try:
                defers.extend(member.listen(cage, callback))
            except Exception as e:
                logging.exception("Listener miner failed: %s" % \
                                    member.__class__.__name__)

        for canary in cage:
            canary.release()
        return defers

class ListenerMinersFactory:
    def __init__(self, clients_repository, results_repository):
        self.clients_repository = clients_repository
        self.results_repository = results_repository

    def new(self, minerClass, client_id):
        return minerClass(self.clients_repository, \
                          self.results_repository, \
                          client_id)
