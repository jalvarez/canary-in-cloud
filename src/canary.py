import urllib
import time
import datetime

class Canary:
	def __init__(self, result_table, url):
		self.result_table = result_table
		self.url = url

	def check(self):
		self.result = {	'timestamp': str(time.time())
						,'timestamp_iso': datetime.datetime.now().isoformat() 
						,'status_code': 0
						,'duration': 0
				 		}

		try:	
			start_time = time.clock()
			response = urllib.urlopen(self.url)
			self.result['status_code'] = response.getcode()
			end_time = time.clock()
			self.result['duration'] = int((end_time - start_time) * 1000)
		except IOError:
			self.result['status_code'] = 404 # Not found
		except:
			self.result['status_code'] = 418 # I'm a teapot (RFC 2324)
		finally:
			try:
				response.close()
			except:
				None

		return self.result

	def register_response(self):
		if not hasattr(self, 'result'):
			raise RegisterWithoutCheckError()
		self.result_table.put_item(Item={ 'url': self.url
										,'time': self.result['timestamp']
										,'timestamp_iso': self.result['timestamp_iso']
										,'status_code': self.result['status_code']
										,'response_ms': self.result['duration']
										})

class RegisterWithoutCheckError(Exception):
	pass
