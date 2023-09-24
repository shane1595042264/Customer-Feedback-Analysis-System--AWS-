
import boto3

client = boto3.client('quicksight')
response = client.list_dashboards(AwsAccountId='YOUR_AWS_ACCOUNT_ID')
print(response)
