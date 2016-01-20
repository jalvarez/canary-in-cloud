from AWS_context import AWSContext
import logging

def scan_handler(event, handler_context):
	ctx = AWSContext()
	for client in ctx.clients_repository.get_clients():
		logging.info("Scanning urls of %s" % client['name'])
		for client_url in ctx.clients_repository.get_client_urls(client['client_id']):
			logging.info("Check url: %s" % client_url['url'])
			canary = ctx.canary_factory.new(client_url['url'])
			canary.check()
			canary.register_response()
	
	return 'Ok'
