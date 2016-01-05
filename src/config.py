from boto3.dynamodb.conditions import Key
import dateutil.parser

class Config:

	def __init__(self, config_table, enviroment):
		self.parameters = {}

		response = config_table.query(KeyConditionExpression=Key('enviroment').eq(enviroment))
		for param in response['Items']:
			if param['type'] == 'string':
				self.parameters[param['parameter']] = param['string_value']
			elif param['type'] == 'date':
				self.parameters[param['parameter']] = dateutil.parser.parse(param['date_value']) 
			elif param['type'] == 'number':
				self.parameters[param['parameter']] = param['number_value'] 
			elif param['type'] == 'integer':
				self.parameters[param['parameter']] = int(param['number_value'] )

	def get(self, parameter_name):
		return self.parameters[parameter_name]
