import boto3
from boto3.dynamodb.conditions import Key
import src

dynamodb = boto3.resource('dynamodb')

scan_result_table = dynamodb.Table('scan_result')

url = 'http://www.google.com'

response = scan_result_table.query(
			KeyConditionExpression=Key('url').eq(url),
			Limit=1, 
			ScanIndexForward=False)

items = response['Items']
print(items)
