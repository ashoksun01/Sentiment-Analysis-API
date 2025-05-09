import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from numpy.testing import assert_almost_equal

from src.main import app
from src.main import SentimentRequest, SentimentResponse, Sentiment


@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c


def test_predict(client):
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/bulk-predict",
        json=data,
    )
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json()["predictions"], list)
    assert isinstance(response.json()["predictions"][0], list)
    assert isinstance(response.json()["predictions"][0][0], dict)
    assert isinstance(response.json()["predictions"][1][0], dict)
    assert set(response.json()["predictions"][0][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][0][1].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][1].keys()) == {"label", "score"}
    assert response.json()["predictions"][0][1]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][0]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][1]["label"] == "NEGATIVE"
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][0]["score"], 0.936, decimal=1
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][1]["score"], 0.064, decimal=1
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][0]["score"], 0.997, decimal=1
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][1]["score"], 0.003, decimal=1
        )
        is None
    )

def test_sentiment_request_model_empty():
    data = {"text": []}
    sentiment_request = SentimentRequest(**data)
    assert sentiment_request.text == []

def test_sentiment_request_model_valid():
    data = {"text": ["The weather is great outside!"]}
    sentiment_request = SentimentRequest(**data)
    assert sentiment_request.text == ["The weather is great outside!"]

def test_sentiment_response_model_empty():
    data = {"predictions": [[]]}
    sentiment_response = SentimentResponse(**data)
    assert sentiment_response.predictions == [[]]

def test_sentiment_response_model_valid():
    prediction_data = [
        [{"label": "POSITIVE", "score": 0.95}]
    ]
    sentiment_response = SentimentResponse(predictions=[
        [Sentiment(label=sentiment["label"], score=sentiment["score"]) for sentiment in sentiments]
        for sentiments in prediction_data
    ])
    assert sentiment_response.dict()["predictions"] == prediction_data

def test_bulk_predict_valid_data(client):
    data = {"text": ["Awesome!", "Horrible!"]}
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2

def test_bulk_predict_invalid_data_type(client):
    data = {"text": "this is a string"}
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 422

def test_bulk_predict_missing_data(client):
    data = {}
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 422

def test_bulk_predict_load(client):
    data = {"text": ["Amazing!"] * 100}
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 100
    assert all(isinstance(pred[0], dict) for pred in response.json()["predictions"])

def test_predict_special_characters(client):
    data = {"text": ["!@#$%^&*()"]}
    response = client.post("/bulk-predict", json=data)
    assert response.status_code == 200

def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root(client):
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_swagger_ui(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text

def test_openapi_json(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "info" in response.json()

def test_openapi_version(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["openapi"] >= "3.0.0"

def test_invalid_endpoint(client):
    response = client.get("/invalid_route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

