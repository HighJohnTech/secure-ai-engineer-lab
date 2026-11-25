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
