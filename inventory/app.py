from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# будет временная in-memory "база"
items = {"apple": 10}

class Item(BaseModel):
    name: str
    quantity: int

@app.post("/items")
def create_item(item: Item):
    items[item.name] = item.quantity
    return {"status": "ok", "item": item}

@app.get("/items")
def list_items():
    return items
