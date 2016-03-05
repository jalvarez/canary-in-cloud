from listener_miners import ListenerMinersFactory
from listener_miners import ListenerMinerTeam
from listener_miners import RecoveryListenerMiner
from listener_miners import NotOkListenerMiner

class ListenAndAlertService:
    def __init__(self, clients_repository, results_repository, canary_factory):
        self.canary_factory = canary_factory
        self.clients_repository = clients_repository
        self.listener_miners_factory = ListenerMinersFactory( \
                                                        clients_repository, \
                                                        results_repository)

    def listen_and_alert(self, client_id):
        cage = map(lambda url: self.canary_factory.new(url['url']), \
                   self.clients_repository.get_client_urls(client_id))
        listener_miner_team = ListenerMinerTeam()
        for miner in [NotOkListenerMiner, RecoveryListenerMiner]:
            listener_miner_team.add_member(self.listener_miners_factory.new( \
                                                                    miner, \
                                                                    client_id))

        return listener_miner_team.listen(cage, lambda _: None)
