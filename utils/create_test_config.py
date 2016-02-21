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
    config_table.put_item(Item = {  'enviroment': enviroment
                                    ,'parameter': parameter
                                    ,'number_value': value
                                    ,'type': value_type
                                })

def insert_function_enviroment(function_name, enviroment):
    func_enviroment_table = dynamodb.Table('function_enviroment')
    func_enviroment_table.put_item(Item = {  'function_name': function_name
                                            ,'enviroment': enviroment
                                            })
    
def insert_config(enviroment):
    config_table = dynamodb.Table('config')
    insert_string_parameter(config_table, enviroment, 'SMTP_HOST', 'smtp.gmail.com')
    insert_integer_parameter(config_table, enviroment, 'SMTP_PORT', 587)
    insert_string_parameter(config_table, enviroment, 'SMTP_USER', 'canaryincloud@gmail.com')
    insert_string_parameter(config_table, enviroment, 'SMTP_PASS', '')
    insert_integer_parameter(config_table, enviroment, 'TIMEOUT_SEC', 5)

def insert_client(client_id, name, email):
    client_table = dynamodb.Table('clients')
    client_table.put_item(Item = {  'client_id': client_id
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
insert_function_enviroment('CanaryInCloudScan_TEST', 'TEST')
insert_config('TEST')
insert_client('test', 'Test client', 'juanmi.alvarez@gmail.com')
insert_url2scan('test', 'http://www.mutuatfe.es')
insert_url2scan('test', 'https://online.mutuatfe.es')
insert_url2scan('test', 'https://clientes.mutuatfe.es')
