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

class ResultsRepository:
    def __init__(self, result_table):
        self.result_table = result_table

    def resultsSerie_by_url(self, url):
        return ResultsSerie(url, self.result_table)

    def count_results_by_url(self, url):
        response = self.result_table.scan(Select='COUNT')
        count = response['Count']
        while ('LastEvaluatedKey' in response):
            response = self.result_table.scan(Select='COUNT', \
                                ExclusiveStartKey=response['LastEvaluatedKey'])
            count += response['Count']
        return count
