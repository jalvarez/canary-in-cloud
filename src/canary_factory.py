from canary import Canary

class CanaryFactory:
	def __init__(self, result_table, agent):
		self.result_table = result_table
        self.agent = agent

	def new(self, url):
		return Canary(self.result_table, self.agent, url)
