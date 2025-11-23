from unittest.mock import patch
from httpx import Response


def test_predict_no_jwt(client):
    res = client.post("/predict", json={"text": "hello"})
    assert res.status_code == 403


def test_predict_invalid_jwt(client):
    res = client.post("/predict", json={"text": "hello"},
                      headers={"Authorization": "Bearer fake"})
    assert res.status_code == 401


@patch("routes.predict_routes.HUGGINGFACE_API_KEY", None)
def test_predict_missing_api_key(client, auth_headers):
    res = client.post("/predict", json={"text": "hello"}, headers=auth_headers)
    assert res.status_code == 500


positive = [[{"label": "5 stars", "score": 0.9}]]
negative = [[{"label": "1 star", "score": 0.8}]]
neutral = [[{"label": "3 stars", "score": 0.6}]]


@patch("routes.predict_routes.query_huggingface", return_value=positive)
def test_predict_positive(mock_hf, client, auth_headers):
    res = client.post("/predict", json={"text": "I love it"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["sentiment"] == positive


@patch("routes.predict_routes.query_huggingface", return_value=negative)
def test_predict_negative(mock_hf, client, auth_headers):
    res = client.post("/predict", json={"text": "I hate it"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["sentiment"] == negative


@patch("routes.predict_routes.query_huggingface", return_value=neutral)
def test_predict_neutral(mock_hf, client, auth_headers):
    res = client.post("/predict", json={"text": "meh"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["sentiment"] == neutral