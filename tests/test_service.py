import pytest
from inventory.models import Item
from inventory.storage import InventoryStorage
from inventory.services_db import InventoryService

@pytest.mark.asyncio
async def test_service_create_get_delete():
    storage = InventoryStorage()
    service = InventoryService(storage)

    item = Item(name="banana", quantity=10)
    created = await service.create_item(item)
    assert created.name == "banana"

    fetched = await service.get_item("banana")
    assert fetched.quantity == 10

    deleted_name = await service.delete_item("banana")
    assert deleted_name == "banana"

    # Проверяем, что элемент реально удалился
    with pytest.raises(ValueError):
        await service.get_item("banana")
