import boto3
from clients_repository import ClientsRepository
from canary_factory import CanaryFactory
from config import Config
from results_repository import ResultsRepository
from listen_and_alert_service import ListenAndAlertService
from twisted.internet import reactor
from twisted.web.client import Agent
from web_client_context import WebClientContextFactory
from enviroments_repository import EnviromentsRepository

class AWSContext():
    def __init__(self, function_name):
        self.init_dynamodb()
        self.init_enviroments_repository()
        self.enviroment = self.enviroments_repository. \
                                    get_enviroment_by_function(function_name)
        self.init_config()
        self.init_clients_repository()
        self.init_canary_factory()
        self.init_results_repository()
        self.init_listen_and_alert_service()

    def init_dynamodb(self):
        self.dynamodb = boto3.resource('dynamodb')

    def init_enviroments_repository(self):
        enviroment_table = self.dynamodb.Table('function_enviroment')
        self.enviroments_repository = EnviromentsRepository(enviroment_table)

    def init_config(self):
        self.config = Config(self.dynamodb.Table('config'), self.enviroment)

    def init_clients_repository(self):
        clients_table = self.dynamodb.Table('clients')
        url2scan_table = self.dynamodb.Table('url2scan')
        self.clients_repository = ClientsRepository(self.enviroment, \
                                                    clients_table, \
                                                    url2scan_table, \
                                                    self.config)

    def init_results_repository(self):
        results_table = self.dynamodb.Table('scan_result')
        self.results_repository = ResultsRepository(results_table)

    def init_canary_factory(self):
        scan_result_table = self.dynamodb.Table('scan_result')
        context_factory = WebClientContextFactory()
        agent = Agent(reactor, context_factory, \
                      connectTimeout=self.config.get('TIMEOUT_SEC'))
        self.canary_factory = CanaryFactory(scan_result_table, agent)

    def init_listen_and_alert_service(self):
        self.listen_and_alert_service = ListenAndAlertService( \
                                                    self.clients_repository, \
                                                    self.results_repository, \
                                                    self.canary_factory)
