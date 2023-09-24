import psycopg2  # For connecting to Redshift
import pymysql   # For connecting to RDS
import os
from dotenv import load_dotenv
# RDS configurations
load_dotenv()
rds_host = os.getenv("RDS_HOST")
rds_user = os.getenv("RDS_USER")
rds_password = os.getenv("RDS_PASSWORD")
rds_db = os.getenv("RDS_DATABASE")

# Redshift configurations
redshift_host = os.getenv("REDSHIFT_HOST")
redshift_user = os.getenv("REDSHIFT_USER")
redshift_password = os.getenv("REDSHIFT_PASSWORD")
redshift_db = os.getenv("REDSHIFT_DB")

# Connect to RDS
rds_conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db)
rds_cursor = rds_conn.cursor()

# Extract data from RDS
select_query = "SELECT * FROM feedback_table"  # Modify based on your needs
rds_cursor.execute(select_query)
data = rds_cursor.fetchall()

# Process data (this is where you'd perform any cleaning, transformation, etc.)
# For this example, we'll just assume the data needs no processing

# Connect to Redshift
redshift_conn = psycopg2.connect(dbname=redshift_db, user=redshift_user, password=redshift_password, host=redshift_host)
redshift_cursor = redshift_conn.cursor()

# Load data into Redshift
for row in data:
    insert_query = "INSERT INTO redshift_feedback_table VALUES (%s)"  # Modify based on your schema
    redshift_cursor.execute(insert_query, row)

redshift_conn.commit()
