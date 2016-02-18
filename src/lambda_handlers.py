from AWS_context import AWSContext
import logging
from twisted.internet import reactor, defer
from sys import exit

def _errors_handler(failure):
    failure.trap(Exception)
    reactor.stop()
    try:
        failure.raiseException()
    except Exception as e:
        logging.exception(e)

def _get_all_defers_listen_and_alert(finish_callback):
    ctx = AWSContext('TEST')
    defers = []
    for client in ctx.clients_repository.get_clients():
        logging.info("Scanning urls of %s" % client['name'])
        defers.extend(ctx.listen_and_alert_service.listen_and_alert( \
                                                           client['client_id']))

    return defer.gatherResults(defers)\
            .addCallback(finish_callback)\
            .addErrback(_errors_handler)

def scan_handler(event, handler_context):
    _get_all_defers_listen_and_alert(lambda _: reactor.stop())
    reactor.run()
    exit(0)
    return 'Ok'
