from boto3.dynamodb.conditions import Key

class ResultsSerie:
	def __init__(self, url, result_table):
		self.url = url
		self.result_table = result_table

	def last_result(self):
		response = self.result_table.query(
							KeyConditionExpression=Key('url').eq(self.url),
							Limit=1, 
							ScanIndexForward=False)

		items = response['Items']
		if (len(items) == 0):
			return None
		return items[0]
