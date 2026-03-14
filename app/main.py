from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Items API",
    version="1.0.0",
    description="A minimal FastAPI service demonstrating CRUD operations on an in-memory item store.",
)

# --- Models ---

class ItemCreate(BaseModel):
    name: str
    description: str


class Item(BaseModel):
    id: int
    name: str
    description: str


# --- In-memory store ---

items: list[Item] = [
    Item(id=1, name="Widget Alpha",   description="A small but mighty widget."),
    Item(id=2, name="Gadget Beta",    description="Multi-purpose gadget for everyday use."),
    Item(id=3, name="Doohickey Gamma", description="The indispensable doohickey."),
]

_next_id: int = len(items) + 1


# --- Endpoints ---

@app.get("/health", tags=["meta"])
def health_check() -> dict:
    """Returns service liveness status."""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/items", response_model=list[Item], tags=["items"])
def get_items() -> list[Item]:
    """Returns all items in the store."""
    return items


@app.post("/items", response_model=Item, status_code=201, tags=["items"])
def create_item(payload: ItemCreate) -> Item:
    """Adds a new item to the store and returns it."""
    global _next_id
    item = Item(id=_next_id, name=payload.name, description=payload.description)
    items.append(item)
    _next_id += 1
    return item
