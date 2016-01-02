import boto3
import datetime

dynamodb = boto3.resource('dynamodb')

def now_json():
	return datetime.datetime.now().isoformat()

def insert_url2scan(client_id, url):
	url2scan_table = dynamodb.Table('url2scan')
	url2scan_table.put_item(Item = { 'client_id': client_id
									,'url': url
									,'active': True
									,'start_scan_date': now_json()
									})

insert_url2scan('test', 'http://www.google.com')
