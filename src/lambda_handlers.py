from AWS_context import AWSContext
import logging

def scan_handler(event, handler_context):
	ctx = AWSContext('TEST')
	for client in ctx.clients_repository.get_clients():
		logging.info("Scanning urls of %s" % client['name'])
		ctx.listen_and_alert_service.listen_and_alert(client['client_id'])
	
	return 'Ok'
