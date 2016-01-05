import boto3
import datetime

dynamodb = boto3.resource('dynamodb')

def now_json():
	return datetime.datetime.now().isoformat()

def insert_number_parameter(config_table, enviroment, parameter, value):
	insert_parameter(config_table, enviroment, parameter, value, 'number')

def insert_integer_parameter(config_table, enviroment, parameter, value):
	insert_parameter(config_table, enviroment, parameter, value, 'integer')

def insert_date_parameter(config_table, enviroment, parameter, value):
	insert_parameter(config_table, enviroment, parameter, value, 'date')

def insert_string_parameter(config_table, enviroment, parameter, value):
	insert_parameter(config_table, enviroment, parameter, value, 'string')

def insert_parameter(config_table, enviroment, parameter, value, value_type):
	config_table.put_item(Item = {	'enviroment': enviroment
									,'parameter': parameter
									,'number_value': value
									,'type': value_type
								})

def insert_config():
	config_table = dynamodb.Table('config')
	insert_string_parameter(config_table, 'TEST', 'SMTP_HOST', 'smtp.gmail.com')
	insert_integer_parameter(config_table, 'TEST', 'SMTP_PORT', 587)
	insert_string_parameter(config_table, 'TEST', 'SMTP_USER', 'canaryincloud@gmail.com')
	insert_string_parameter(config_table, 'TEST', 'SMTP_PASS', '')

def insert_client(client_id, name, email):
	client_table = dynamodb.Table('clients')
	client_table.put_item(Item = { 	'client_id': client_id
									,'name': name
									,'creation_date': now_json()
									,'email': email 
									})

def insert_url2scan(client_id, url):
	url2scan_table = dynamodb.Table('url2scan')
	url2scan_table.put_item(Item = { 'client_id': client_id
									,'url': url
									,'active': True
									,'start_scan_date': now_json()
									})

insert_config()
insert_client('test', 'Test client', 'juanmi.alvarez@gmail.com')
insert_url2scan('test', 'http://www.google.com')
