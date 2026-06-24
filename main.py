from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import boto3
import uuid
import os


from sqlalchemy.orm import Session
from db import SessionLocal
from models import Customer
from schemas import CustomerCreate, CustomerResponse
from typing import List


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

BUCKET = os.getenv("BUCKET_NAME")
s3 = boto3.client(
    "s3",
    region_name="ap-southeast-2"
)

MAX_SIZE = 10 * 1024 * 1024


@app.get("/")
def home():
    return {
        "message": "FastAPI running on ECS alb PINAKI 2"
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if len(contents) > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large"
            )

        key = f"raw/{uuid.uuid4()}-{file.filename}"

        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=contents
        )

        return {
            "message": "Uploaded",
            "file_key": key
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

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

@app.post("/customers", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


@app.get("/customers", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers
