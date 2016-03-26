from AWS_context import AWSContext
from decimal_encoder import DecimalEncoder
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
        
    def _results_handler(self, event):
        results_repository = self.ctx.results_repository
        clients_repository = self.ctx.clients_repository
        client_id = event['client_id']
        url_number = int(event['url_number'])
        if ('n_items' in event):
            n_last = int(event['n_items'])
        else:
            n_last = 100
        urls = clients_repository.get_client_urls(client_id)
        url = urls[url_number]['url']
        from_date = None
        if ('from' in event):
            from_date = event['from']
        results_serie = results_repository.resultsSerie_by_url(url)
        return json.dumps(results_serie.n_last(n_last, from_date), \
                          cls=DecimalEncoder)

def lambda_api_handler(event, handler_context):
    ctx = AWSContext(handler_context.function_name)
    api = CanaryInCloudAPI(ctx)
    api_method = event['api_method']
    return api.handler(api_method, event)

