import boto3
import src

dynamodb = boto3.resource('dynamodb')

scan_result_table = dynamodb.Table('scan_result')

url = 'http://www.google.com'
canary = src.Canary(scan_result_table, url)

result = canary.check()
canary.register_response()

print "Registrado check de %s: %d (%d ms)" % (url, result['code'], result['duration'])
