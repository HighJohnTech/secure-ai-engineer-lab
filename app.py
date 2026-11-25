
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Secure AI Engineer Lab")


@app.get("/")
def home():
    return {
        "message": "Welcome to my AI Engineering Lab!",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


class IntakeRequest(BaseModel):
    business: str = Field(min_length=2)
    question: str = Field(min_length=5)


@app.post("/intake")
def intake(request: IntakeRequest):
    return {
        "business": request.business,
        "received": True,
        "next_step": "review"
    }
