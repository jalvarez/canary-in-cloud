import urllib
import time
import datetime
import logging
from functools import partial
from twisted.web.http_headers import Headers
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class Canary:
    def __init__(self, result_table, agent, url):
        self.AGENT_HEADERS = Headers({'User-Agent:': ['Canary-in-cloud']})
        self.result_table = result_table
        self.agent = agent
        self.url = url
        self.request = None

    def _response_2_result(self, response):
        return { 'status_code': response.code }

    def _check_response(self, callback, result):
        self.result['status_code'] = result['status_code']
        start_time = self.result['start_time']
        end_time = time.clock()
        self.result['duration'] = int((end_time - start_time) * 1000)
        return callback(self.result)

    def _check_failure(self, callback, failure):
        failure.trap(Exception)
        if (failure.check(DNSLookupError)):
            self.result['status_code'] = 404
        elif (failure.check(TimeoutError)):
            self.result['status_code'] = 408
        else:
            logging.error(failure.getErrorMessage())
            logging.error(failure.getBriefTraceback())
            self.result['status_code'] = 418 # I'm a teapot (RFC 2324)
        return callback(self.result)

    def _get_safe_url(self):
        if (isinstance(self.url, unicode)):
            return self.url.encode('ascii', 'ignore')
        return self.url

    def _add_callback_to_request(self, request, callback):
        request.addCallback(partial(self._check_response, callback))
        request.addErrback(partial(self._check_failure, callback))

    def _create_request(self, callback):
        request = self.agent.request('GET', self._get_safe_url(), \
                                     self.AGENT_HEADERS, None)
        request.addCallback(self._response_2_result)
        self._add_callback_to_request(request, callback)
        return request

    def check(self, check_callback):
        if (not self.request):
            now = datetime.datetime.now()
            self.result = { 'url': self.url
                            ,'timestamp': str(time.time())
                            ,'timestamp_iso': now.isoformat() 
                            ,'status_code': 0
                            ,'duration': 0
                            ,'start_time': time.clock()
                            }

            self.request = self._create_request(check_callback)
        else:
            self._add_callback_to_request(self.request, check_callback)
        return self.request

    def register_response(self, result_check=None):
        if not hasattr(self, 'result'):
            raise RegisterWithoutCheckError()
        self.result_table.put_item(Item={ 'url': self.url
                                  ,'time': self.result['timestamp']
                                  ,'timestamp_iso': self.result['timestamp_iso']
                                  ,'status_code': self.result['status_code']
                                  ,'response_ms': self.result['duration']
                                  })
        return result_check

    def check_and_register(self, after_check_callback):
        not_has_register_callback = (not self.request)
        request = self.check(after_check_callback)
        return request

    def release(self):
        self.request.addCallback(self.register_response)


class RegisterWithoutCheckError(Exception):
    pass
