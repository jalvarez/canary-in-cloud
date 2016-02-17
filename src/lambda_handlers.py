from AWS_context import AWSContext
import logging
from twisted.internet import reactor, defer

def _errors_handler(failure):
    failure.trap(Exception)
    try:
        failure.raiseException()
    except Exception(e):
        logging.exception(e)

def scan_handler(event, handler_context):
    ctx = AWSContext('TEST')
    defers = []
    for client in ctx.clients_repository.get_clients():
        logging.info("Scanning urls of %s" % client['name'])
        defers.extend(ctx.listen_and_alert_service.listen_and_alert( \
                                                           client['client_id']))

    defer.gatherResults(defers).addErrback(_errors_handler)
    reactor.run()
    return 'Ok'
