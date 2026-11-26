import httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
	response = client.get("/health")
	assert response.status_code == 200
	assert response.json() == {"status": "ok"}


def test_intake_valid():
	response = client.post("/intake", json={
		"business": "High John Technology",
		"question": "How can AI automate support?"
	})

	assert response.status_code == 200
	assert response.json()["received"] is True
	assert response.json()["business"] == "High John Technology"


def test_intake_invalid():
	response = client.post("/intake", json={
		"business": "H",
		"question": "Hi"
	})

	assert response.status_code == 422

def test_ai_chat_success():
    with patch("app.httpx.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "message": {
                "content": "AI engineers build intelligent applications."
            }
        }

        response = client.post("/ai/chat", json={
            "message": "What does an AI engineer do?"
        })

    assert response.status_code == 200
    assert response.json()["model"] == "gemma4:latest"
    assert response.json()["answer"] == (
        "AI engineers build intelligent applications."
    )


def test_ai_chat_invalid_message():
    response = client.post("/ai/chat", json={
        "message": "X"
    })

    assert response.status_code == 422


def test_ai_chat_connection_failure():
    with patch(
        "app.httpx.post",
        side_effect=httpx.ConnectError("Connection refused")
    ):
        response = client.post("/ai/chat", json={
            "message": "Explain artificial intelligence."
        })

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Local Ollama model is unavailable."
    )

def test_ai_chat_empty_response():
    with patch("app.httpx.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "message": {"content": ""}
        }

        response = client.post("/ai/chat", json={
            "message": "Explain machine learning."
        })

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Local Ollama returned an empty answer."
    )
