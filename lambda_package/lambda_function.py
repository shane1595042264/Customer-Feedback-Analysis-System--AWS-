import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Get the bucket and file key from the Lambda event trigger
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')
    
    # Read the content with pandas
    data = pd.read_csv(StringIO(file_content))
    
    # Simple preprocessing
    data = data.dropna()  # Remove rows with NaN values
    data.columns = [col.lower() for col in data.columns]  # Convert headers to lowercase
    
    # Convert the dataframe back to CSV and upload back to S3
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket="cleaned-data-bucket-shane", Key=key, Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': f'Processed file {key} and saved to cleaned-data-bucket-shane'
    }
