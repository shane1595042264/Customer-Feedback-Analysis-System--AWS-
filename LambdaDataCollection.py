import json
import pymysql
import os
from dotenv import load_dotenv



def lambda_handler(event, context):
    # Extract data from the event object
    feedback_data = event['body']

    # Database configurations (should use environment variables or AWS Secrets Manager)
    load_dotenv()
    rds_host = os.getenv("RDS_HOST")
    rds_user = os.getenv("RDS_USER")
    rds_password = os.getenv("RDS_PASSWORD")
    rds_db = os.getenv("RDS_DATABASE")
    
    # Connect to the database
    conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db, connect_timeout=5)
    cursor = conn.cursor()

    # Insert data into the database
    insert_query = "INSERT INTO feedback_table(feedback_column) VALUES (%s)"  # Modify based on your schema
    cursor.execute(insert_query, (feedback_data,))
    conn.commit()

    return {
        'statusCode': 200,
        'body': json.dumps('Feedback received!')
    }
