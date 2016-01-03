import urllib
import time

def check_url(url):
	result = {	 'code': 0
				,'time': 0
			 }

	try:	
		start_time = time.clock()
		response = urllib.urlopen(url)
		result['code'] = response.getcode()
		end_time = time.clock()
		result['time'] = (end_time - start_time) * 1000
	except IOError:
		result['code'] = 404 # Not found
	except:
		result['code'] = 418 # I'm a teapot (RFC 2324)
	finally:
		try:
			reponse.close()
		except:
			None

	return result

def register_response(url, status_code, response_ms):
	result_table.put_item(Item={ 'url': url
								,'time': 0 
								,'status_code': response_code
								,'response_ms': response_ms
								})
