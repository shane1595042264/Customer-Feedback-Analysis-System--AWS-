import json
import boto3
import psycopg2
import os
from dotenv import load_dotenv
def lambda_handler(event, context):
    load_dotenv()
    # Redshift configurations
    redshift_host = os.getenv("REDSHIFT_HOST")
    redshift_user = os.getenv("REDSHIFT_USER")
    redshift_password = os.getenv("REDSHIFT_PASSWORD")
    redshift_db = os.getenv("REDSHIFT_DB")

    # Connect to Redshift
    redshift_conn = psycopg2.connect(dbname=redshift_db, user=redshift_user, password=redshift_password, host=redshift_host)
    redshift_cursor = redshift_conn.cursor()

    # Query data from Redshift
    select_query = "SELECT insight_column FROM redshift_feedback_table"  # Modify based on your needs
    redshift_cursor.execute(select_query)
    insights = redshift_cursor.fetchall()

    # Store insights in S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket="your_bucket_name", Key="insights.json", Body=json.dumps(insights))

    return {
        'statusCode': 200,
        'body': json.dumps('Insights stored in S3!')
    }
