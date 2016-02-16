from twisted.internet import reactor, defer
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.error import TimeoutError

agent = Agent(reactor, connectTimeout=0.5)

def cbFinish(url, response):
	print "%s: Finish received: %s" % (url, response.code)
	return response.code

def cbError(url, failure):
	failure.trap(Exception)
	print "%s: Error" % (url)
	return 0

def createRequest(url):
	d = agent.request('GET', url,
						Headers({'User-Agent': ['Twisted Web Client Example']}),
						None)
	d.addCallback(lambda x: cbFinish(url, x)) \
		.addErrback(lambda x: cbError(url, x))
	return d

urls = ['http://www.google.com'\
		,'http://www.yahoo.com'\
		,'http://localhost:8888'\
		]

requests = [createRequest(url) for url in urls]

def cbFinishAll(responses):
	for response in responses:
		print "Finish received: %s" % response
	reactor.stop()

def cbErrorAll(failure):
	print "Error received: %s" % failure
	failure.trap(Exception)
	reactor.stop()

defer.gatherResults(requests, consumeErrors=True)\
		.addCallback(cbFinishAll)\
		.addErrback(cbErrorAll)
		
reactor.run()
