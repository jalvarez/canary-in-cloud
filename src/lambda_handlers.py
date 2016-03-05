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

def _get_all_defers_listen_and_alert(ctx, finish_callback, error_callback=None):
    defers = []
    for client in ctx.clients_repository.get_clients():
        logging.info("Scanning urls of %s" % client['name'])
        defers.extend(ctx.listen_and_alert_service.listen_and_alert( \
                                                           client['client_id']))

    result_defer = defer.gatherResults(defers).addCallback(finish_callback)
    if (error_callback):
        result_defer.addErrback(error_callback)
    return result_defer

def scan_handler(event, handler_context):
    ctx = AWSContext(handler_context.function_name)
    _get_all_defers_listen_and_alert(ctx, \
                                     lambda _: reactor.stop(), \
                                     _errors_handler)
    reactor.run()
    exit(0)
    return 'Ok'
