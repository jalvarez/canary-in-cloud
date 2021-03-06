import boto3

dynamodb = boto3.resource('dynamodb')

DEFAULT_PROVISIONED_THROUGHPUT = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
}

def create_url2scan_table():
    table = dynamodb.create_table(
        TableName='url2scan',
        KeySchema=[
            {
                'AttributeName': 'client_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'url',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'client_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput=DEFAULT_PROVISIONED_THROUGHPUT
    )

def create_scan_result_table():
    table = dynamodb.create_table(
        TableName='scan_result',
        KeySchema=[
            {
                'AttributeName': 'url',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput=DEFAULT_PROVISIONED_THROUGHPUT
    )

def create_clients_table():
    table = dynamodb.create_table(
        TableName='clients',
        KeySchema=[
            {
                'AttributeName': 'enviroment',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'client_id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'enviroment',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'client_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput=DEFAULT_PROVISIONED_THROUGHPUT
    )
    
def create_config_table():
    table = dynamodb.create_table(
        TableName='config',
        KeySchema=[
            {
                'AttributeName': 'enviroment',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'parameter',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'enviroment',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'parameter',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput=DEFAULT_PROVISIONED_THROUGHPUT
    )
    
def create_function_enviroment_table():
    table = dynamodb.create_table(
        TableName='function_enviroment',
        KeySchema=[
            {
                'AttributeName': 'function_name',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'function_name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput=DEFAULT_PROVISIONED_THROUGHPUT
    )
    
create_url2scan_table()
create_scan_result_table()
create_clients_table()
create_config_table()
create_function_enviroment_table()
