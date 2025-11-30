from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from .models_orm import ItemORM
from .models import Item

class InventoryServiceDB:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(self, item: Item) -> Item:
        result = await self.session.execute(select(ItemORM).where(ItemORM.name == item.name))
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Item already exists")
        orm_item = ItemORM(name=item.name, quantity=item.quantity)
        self.session.add(orm_item)
        await self.session.commit()
        await self.session.refresh(orm_item)
        return Item(name=orm_item.name, quantity=orm_item.quantity)

    async def get_item(self, name: str) -> Item:
        result = await self.session.execute(select(ItemORM).where(ItemORM.name == name))
        orm_item = result.scalar_one_or_none()
        if not orm_item:
            raise ValueError("Item not found")
        return Item(name=orm_item.name, quantity=orm_item.quantity)

    async def list_items(self):
        result = await self.session.execute(select(ItemORM))
        items = result.scalars().all()
        return [Item(name=i.name, quantity=i.quantity) for i in items]

    async def delete_item(self, name: str):
        result = await self.session.execute(select(ItemORM).where(ItemORM.name == name))
        orm_item = result.scalar_one_or_none()
        if not orm_item:
            raise ValueError("Item not found")
        await self.session.delete(orm_item)
        await self.session.commit()
        return name
