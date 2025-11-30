from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Item
from .services_db import InventoryServiceDB
from .db import get_session, engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: закрываем соединения
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# эндпоинт для проверки работоспособности
@app.get("/")
async def root():
    return {"message": "Inventory API is working"}

# эндпоинт POST /items
@app.post("/items", status_code=201)
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    service = InventoryServiceDB(session)
    try:
        return await service.create_item(item)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

# эндпоинт GET /items/{name}
@app.get("/items/{name}")
async def get_item(name: str, session: AsyncSession = Depends(get_session)):
    service = InventoryServiceDB(session)
    try:
        return await service.get_item(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# эндпоинт GET /items
@app.get("/items")
async def list_all_items(session: AsyncSession = Depends(get_session)):
    service = InventoryServiceDB(session)
    return await service.list_items()

# эндпоинт DELETE /items/{name}
@app.delete("/items/{name}")
async def delete_item(name: str, session: AsyncSession = Depends(get_session)):
    service = InventoryServiceDB(session)
    try:
        deleted_name = await service.delete_item(name)
        return {"deleted": deleted_name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))