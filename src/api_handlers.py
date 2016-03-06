from AWS_context import AWSContext
import json

def clients_api_handler(event, handler_context):
    ctx = AWSContext(handler_context.function_name)
    clients_repository = ctx.clients_repository
    clients = clients_repository.get_clients()
    return json.dumps(clients)

def client_url_api_handler(event, handler_context):
    ctx = AWSContext(handler_context.function_name)
    clients_repository = ctx.clients_repository
    client_id = event['client_id']
    urls = clients_repository.get_client_urls(client_id)
    return json.dumps(urls)
