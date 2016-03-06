from AWS_context import AWSContext
import json

class CanaryInCloudAPI:
    def __init__(self, ctx):
        self.ctx = ctx

    def handler(self, handler_name, event):
        method = getattr(self, "_%s_handler" % handler_name)
        return method(event)

    def _clients_handler(self, event):
        clients_repository = self.ctx.clients_repository
        clients = clients_repository.get_clients()
        return json.dumps(clients)

    def _client_urls_handler(self, event):
        clients_repository = self.ctx.clients_repository
        client_id = event['client_id']
        urls = clients_repository.get_client_urls(client_id)
        return json.dumps(urls)

def lambda_api_handler(event, handler_context):
    ctx = AWSContext(handler_context.function_name)
    api = CanaryInCloudAPI(ctx)
    api_method = event['api_method']
    return api.handler(api_method, event)

