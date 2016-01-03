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
			}
		],
		AttributeDefinitions=[
			{
				'AttributeName': 'client_id',
				'AttributeType': 'S'
			}
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

create_url2scan_table()
create_scan_result_table()
