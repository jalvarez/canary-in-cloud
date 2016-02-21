from boto3.dynamodb.conditions import Key

class EnviromentsRepository:
    def __init__(self, function_enviroment_table):
        self.function_enviroment_table = function_enviroment_table

    def get_enviroment_by_function(self, function_name):
        envs = self.function_enviroment_table.query(KeyConditionExpression = \
                                        Key('function_name').eq(function_name))
        return envs['Items'][0]['enviroment']
