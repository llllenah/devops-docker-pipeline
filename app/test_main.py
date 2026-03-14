import pytest
from fastapi.testclient import TestClient

from app.main import app, items

client = TestClient(app)


# --- Helpers ---

def reset_items():
    """Reset the in-memory store to a known state between tests."""
    import app.main as m
    m.items = [
        m.Item(id=1, name="Widget Alpha",    description="A small but mighty widget."),
        m.Item(id=2, name="Gadget Beta",     description="Multi-purpose gadget for everyday use."),
        m.Item(id=3, name="Doohickey Gamma", description="The indispensable doohickey."),
    ]
    m._next_id = 4


@pytest.fixture(autouse=True)
def restore_items():
    reset_items()
    yield
    reset_items()


# --- Tests ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_get_items_returns_list():
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_items_has_initial_data():
    response = client.get("/items")
    assert len(response.json()) >= 3


def test_create_item_success():
    payload = {"name": "New Thing", "description": "Brand new item."}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "New Thing"
    assert body["description"] == "Brand new item."
    assert "id" in body


def test_create_item_missing_field():
    payload = {"name": "Incomplete"}  # missing description
    response = client.post("/items", json=payload)
    assert response.status_code == 422


def test_items_count_increases_after_post():
    before = len(client.get("/items").json())
    client.post("/items", json={"name": "Extra", "description": "One more."})
    after = len(client.get("/items").json())
    assert after == before + 1
