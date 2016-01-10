from boto3.dynamodb.conditions import Key

class ClientsRepository:
	def __init__(self, clients_table, url2scan_table):
		self.clients_table = clients_table
		self.url2scan_table = url2scan_table

	def get_client(self, client_id):
		clients = self.clients_table.query(KeyConditionExpression=Key('client_id').eq(client_id))
		return clients['Items'][0]

	def get_client_urls(self, client_id):
		urls = self.url2scan_table.query(KeyConditionExpression=Key('client_id').eq(client_id))
		return urls['Items']

	def get_clients(self):
		clients = self.clients_table.scan()
		return clients['Items']

