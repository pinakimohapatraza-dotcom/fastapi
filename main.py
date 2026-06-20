from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message":"FastAPI running on ECS alb PINAKI 10"
    }