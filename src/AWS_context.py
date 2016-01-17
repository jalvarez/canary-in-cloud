import boto3
from clients_repository import ClientsRepository
from canary_factory import CanaryFactory

class AWSContext():
	def __init__(self):
		self.init_dynamodb()
		self.init_clients_repository()
		self.init_canary_factory()

	def init_dynamodb(self):
		self.dynamodb = boto3.resource('dynamodb')

	def init_clients_repository(self):
		clients_table = self.dynamodb.Table('clients')
		url2scan_table = self.dynamodb.Table('url2scan')
		self.clients_repository = ClientsRepository(clients_table, url2scan_table)

	def init_canary_factory(self):
		scan_result_table = self.dynamodb.Table('scan_result')
		self.canary_factory = CanaryFactory(scan_result_table)
