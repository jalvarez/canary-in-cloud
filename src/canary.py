import urllib
import time
import datetime
from functools import partial
from twisted.web.http_headers import Headers
from twisted.internet.error import DNSLookupError

class Canary:
    def __init__(self, result_table, agent, url):
        self.AGENT_HEADERS = Headers({'User-Agent:': ['Canary-in-cloud']})
        self.result_table = result_table
        self.agent = agent
        self.url = url

    def _check_response(self, callback, response):
        self.result['status_code'] = response.code
        start_time = self.result['start_time']
        end_time = time.clock()
        self.result['duration'] = int((end_time - start_time) * 1000)
        callback(self.result)

    def _check_failure(self, callback, failure):
        failure.trap(Exception)
        if (failure.check(DNSLookupError)):
            self.result['status_code'] = 404
        else:
            self.result['status_code'] = 418 # I'm a teapot (RFC 2324)
        callback(self.result)

    def _create_request(self, callback):
        request = self.agent.request('GET', self.url, self.AGENT_HEADERS, None)
        request.addCallback(partial(self._check_response, callback))
        request.addErrback(partial(self._check_failure, callback))
        return request

    def check(self, check_callback):
        self.result = { 'timestamp': str(time.time())
                        ,'timestamp_iso': datetime.datetime.now().isoformat() 
                        ,'status_code': 0
                        ,'duration': 0
                        ,'start_time': time.clock()
                        }

        request = self._create_request(check_callback)
        return request

    def register_response(self, result=None):
        if not hasattr(self, 'result'):
            raise RegisterWithoutCheckError()
        self.result_table.put_item(Item={ 'url': self.url
                                  ,'time': self.result['timestamp']
                                  ,'timestamp_iso': self.result['timestamp_iso']
                                  ,'status_code': self.result['status_code']
                                  ,'response_ms': self.result['duration']
                                  })

    def check_and_register(self, after_check_callback):
        request = self.check(after_check_callback)
        request.addCallback(self.register_response)
        return request

class RegisterWithoutCheckError(Exception):
    pass
