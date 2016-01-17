from AWS_context import AWSContext

def scan_handler(event, handler_context):
	ctx = AWSContext()
	for client in ctx.clients_repository.get_clients():
		for client_url in ctx.clients_repository.get_client_urls(client['client_id']):
			canary = ctx.canary_factory.new(client_url['url'])
			canary.check()
			canary.register_response()
	
	return 'Ok'
