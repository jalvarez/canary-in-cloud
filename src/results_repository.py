from boto3.dynamodb.conditions import Key
import dateutil.parser
import time

class ResultsSerie:
    def __init__(self, url, result_table):
        self.url = url
        self.result_table = result_table

    def last_result(self):
        items = self.n_last(1)
        if (len(items) == 0):
            return None
        return items[0]

    def _isoformatdate2timestamp(self, datetime_from):
        datetime = dateutil.parser.parse(datetime_from)
        return str(time.mktime(datetime.timetuple()))

    def n_last(self, n_last, from_date=None):
        n_last_items = []
        query_params = { 'KeyConditionExpression': Key('url').eq(self.url), \
                         'Limit': n_last, \
                         'ScanIndexForward': False }

        if (from_date):
            datetime_from = self._isoformatdate2timestamp(from_date)
            query_params['KeyConditionExpression'] = query_params['KeyConditionExpression'] & Key('time').gte(datetime_from)

        while True:
            response = self.result_table.query(**query_params)
            n_last_items.extend(response['Items'])

            if ('LastEvaluatedKey' in response and \
                response['Count'] > query_params['Limit']):
                    query_params['Limit'] -= response['Count']
                    query_params['ExclusiveStartKey'] = \
                                                    response['LastEvaluatedKey']
            else:
                break

        return n_last_items

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
