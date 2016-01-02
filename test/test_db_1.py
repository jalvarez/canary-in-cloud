import boto3

dynamodb = boto3.resource('dynamodb')

url2scan_table = dynamodb.Table('url2scan')

print(url2scan_table.creation_date_time)
