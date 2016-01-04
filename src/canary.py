import urllib
import time
import datetime

class Canary:
	def __init__(self, url):
		self.url = url

	def check(self):
		self.result = {	'timestamp': str(time.time())
						,'timestamp_iso': datetime.datetime.now().isoformat() 
						,'code': 0
						,'duration': 0
				 		}

		try:	
			start_time = time.clock()
			response = urllib.urlopen(self.url)
			self.result['code'] = response.getcode()
			end_time = time.clock()
			self.result['duration'] = int((end_time - start_time) * 1000)
		except IOError:
			self.result['code'] = 404 # Not found
		except:
			self.result['code'] = 418 # I'm a teapot (RFC 2324)
		finally:
			try:
				reponse.close()
			except:
				None

		return self.result

	def register_response(self, result_table):
		result_table.put_item(Item={ 'url': self.url
									,'time': self.result['timestamp']
									,'timestamp_iso': self.result['timestamp_iso']
									,'status_code': self.result['code']
									,'response_ms': self.result['duration']
									})
