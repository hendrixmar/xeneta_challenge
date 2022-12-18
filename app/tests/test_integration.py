import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_date():
    response = client.get("/rates", params={
        "date_from": '2016-01-1'
    })
    assert response.status_code == 200


def test_invalid_date():
    response = client.get("/rates", params={
        "date_from": '2016-30-1'
    })
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{'loc': ['query', 'date_from'], 'msg': 'invalid date format', 'type': 'value_error.date'}]}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/rates?destination=changai", 404, {'detail': "The parameter changai isn't related with any port"}),

    ],
)
def test_rates_retrieval(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
    print(response.json())


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}
