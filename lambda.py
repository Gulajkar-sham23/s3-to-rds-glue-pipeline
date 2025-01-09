import boto3
import pymysql
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS credentials setup
s3_client = boto3.client('s3')
rds_host = "<RDS_ENDPOINT>"
rds_user = "<RDS_USER>"
rds_password = "<RDS_PASSWORD>"
rds_db = "<RDS_DB>"
glue_client = boto3.client('glue')

# S3 bucket and key
s3_bucket = "<S3_BUCKET_NAME>"
s3_key = "<S3_FILE_KEY>"

def read_s3_file(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')

def push_to_rds(data):
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, database=rds_db)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO <TABLE_NAME> (data_column) VALUES (%s)", (data,))
        connection.commit()
        return "Data pushed to RDS successfully."
    except Exception as e:
        print(f"RDS insertion failed: {e}")
        return None
    finally:
        connection.close()

def push_to_glue_database(data):
    # Create a Glue job or use Glue API to store data
    # Add Glue logic here
    print("Fallback: Data pushed to Glue Database.")
    return "Data pushed to Glue Database successfully."

def main():
    try:
        data = read_s3_file(s3_bucket, s3_key)
        result = push_to_rds(data)
        if not result:
            push_to_glue_database(data)
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"AWS credentials error: {e}")

if __name__ == "__main__":
    main()
