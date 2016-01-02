import boto3

dynamodb = boto3.resource('dynamodb')

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
		ProvisionedThroughput={
			'ReadCapacityUnits': 5,
			'WriteCapacityUnits': 5
		}
	)

create_url2scan_table()
