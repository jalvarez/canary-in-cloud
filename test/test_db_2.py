import boto3
from src import canary

#dynamodb = boto3.resource('dynamodb')

#scan_result_table = dynamodb.Table('scan_result')

print canary.check_url('http://www.google.com')
