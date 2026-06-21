import os
import json
import boto3
from fastapi import FastAPI

app = FastAPI()

sqs = boto3.client("sqs", region_name="ap-south-1")

QUEUE_URL = os.getenv("QUEUE_URL")


@app.get("/")
def home():
    return {
        "message": "FastAPI running on ECS alb PINAKI 101"
    }


@app.post("/order")
def create_order(order: dict):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(order)
    )

    return {
        "message": "Order queued",
        "message_id": response["MessageId"]
    }