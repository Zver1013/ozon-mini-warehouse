from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
items: dict[str, int] = {}

class Item(BaseModel):
    name: str
    quantity: int

@app.post("/items", status_code=201)
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=409, detail="Item already exists")
    items[item.name] = item.quantity
    return {"status": "created", "item": item}

@app.get("/items")
async def list_items():
    return items

@app.get("/items/{name}")
async def get_item(name: str):
    if name not in items:
        raise HTTPException(status_code=404, detail="Not found")
    return {"name": name, "quantity": items[name]}

@app.put("/items/{name}")
async def update_item(name: str, item: Item):
    if name not in items:
        raise HTTPException(status_code=404, detail="Not found")
    # allow renaming? for простоты — overwrite quantity only
    items[name] = item.quantity
    return {"status": "updated", "item": {"name": name, "quantity": items[name]}}

@app.delete("/items/{name}", status_code=204)
async def delete_item(name: str):
    if name not in items:
        raise HTTPException(status_code=404, detail="Not found")
    del items[name]
