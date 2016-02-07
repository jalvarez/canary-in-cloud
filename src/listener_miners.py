class ListenerMiner:
	def __init__(self, 	clients_repository, results_repository, \
						canary_factory, client_id):
		self.clients_repository = clients_repository
		self.results_repository = results_repository
		self.canary_factory = canary_factory
		self.client_id = client_id
		self._is_alert = False

	def listen_client_urls(self, listener):
		for url in self.clients_repository.get_client_urls(self.client_id):
			canary = self.canary_factory.new(url)
			listener(canary, url)

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

class NotOkListenerMiner(LastResultListenerMiner):
	def not_ok_listener(self, canary, url):
		canary_check = canary.check()
		last_result = self.get_last_result(url)
		canary.register_response()
		self._is_alert = self.is_result_ok(last_result) and \
							not self.is_result_ok(canary_check)

	def listen(self):
		self.listen_client_urls(self.not_ok_listener)
	
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
