import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')

url2scan_table = dynamodb.Table('url2scan')

print(url2scan_table.creation_date_time)

response = url2scan_table.scan(FilterExpression=Attr('client_id').eq('test')
												& Attr('active').eq(True))

items = response['Items']

print(items)
