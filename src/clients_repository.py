from boto3.dynamodb.conditions import Key

from channel_factory import ChannelFactory

class ClientsRepository:
	def __init__(self, clients_table, url2scan_table, config):
		self.clients_table = clients_table
		self.url2scan_table = url2scan_table
		self.channel_factory = ChannelFactory(config)

	def get_client(self, client_id):
		clients = self.clients_table.query(KeyConditionExpression=Key('client_id').eq(client_id))
		return clients['Items'][0]

	def get_client_urls(self, client_id):
		urls = self.url2scan_table.query(KeyConditionExpression=Key('client_id').eq(client_id))
		return urls['Items']

	def get_clients(self):
		clients = self.clients_table.scan()
		return clients['Items']

	def get_client_channels(self, client_id):
		client = self.get_client(client_id)
		email_channel = self.channel_factory.newEmailChannel(client['email'])
		return [email_channel]
