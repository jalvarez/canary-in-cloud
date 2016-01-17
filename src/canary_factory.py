from canary import Canary

class CanaryFactory:
	def __init__(self, result_table):
		self.result_table = result_table

	def new(self, url):
		return Canary(self.result_table, url)
