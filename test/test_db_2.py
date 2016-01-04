import boto3
import src

dynamodb = boto3.resource('dynamodb')

scan_result_table = dynamodb.Table('scan_result')

url = 'http://www.google.com'
canary = src.Canary(url)

result = canary.check()
canary.register_response(scan_result_table)

print "Registrado check de %s: %d (%d ms)" % (url, result['code'], result['duration'])
