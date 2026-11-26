
import httpx

from fastapi import FastAPI, HTTPException
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


# AI Chat Endpoint

class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=1000)



@app.post("/ai/chat")
def ai_chat(request: ChatRequest):
    try:
        response = httpx.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": "gemma4:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": request.message
                    }
                ],
                "stream": False,
                "think": False,
                "options": {"num_predict": 256}
            },
            timeout=240.0
        )

        response.raise_for_status()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="Local Ollama model is unavailable."
        ) from None

    answer = response.json()["message"]["content"]

    # Reject empty AI responses BEFORE returning success
    if not isinstance(answer, str) or not answer.strip():
        raise HTTPException(
            status_code=502,
            detail="Local Ollama returned an empty answer."
        )

    return {
        "model": "gemma4:latest",
        "answer": answer
    }
