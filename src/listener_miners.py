class ListenerMiner:
	def __init__(self, clients_repository, results_repository, client_id):
		self.clients_repository = clients_repository
		self.results_repository = results_repository
		self.client_id = client_id
		self._is_alert = False

	def listen_client_urls(self, listener):
		for url in self.clients_repository.get_client_urls(self.client_id):
			listener(url)

	def is_alert(self):
		return self._is_alert

class LastResultListenerMiner(ListenerMiner):
	def get_last_result(self, url):
		results_serie = self.results_repository.resultsSerie_by_url(url)
		return results_serie.last_result()

class NotOkListenerMiner(LastResultListenerMiner):
	def not_ok_listener(self, url):
		last_result = self.get_last_result(url)
		self._is_alert = (last_result['status_code'] != 200)

	def listen(self):
		self.listen_client_urls(self.not_ok_listener)
	
class ListenerMinersFactory:
	def __init__(self, clients_repository, results_repository):
		self.clients_repository = clients_repository
		self.results_repository = results_repository

	def new(self, minerClass, client_id):
		return minerClass(self.clients_repository, \
						  self.results_repository, \
						  client_id)
