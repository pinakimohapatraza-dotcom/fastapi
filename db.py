import boto3
import json
from sqlalchemy import create_engine

def get_secret():
    client = boto3.client("secretsmanager", region_name="ap-southeast-2")
    response = client.get_secret_value(
        SecretId="fastapi/rds/customerdb"
    )
    return json.loads(response["SecretString"])

secret = get_secret()

DATABASE_URL = f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}:{secret['port']}/{secret['dbname']}"

engine = create_engine(DATABASE_URL)