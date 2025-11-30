from typing import Dict
from .models import Item

class InventoryStorage:
    def __init__(self):
        self._items: Dict[str, Item] = {}

    def add_item(self, item: Item):
        self._items[item.name] = item

    def get_item(self, name: str):
        return self._items.get(name)

    def delete_item(self, name: str):
        return self._items.pop(name, None)

    def list_items(self):
        return list(self._items.values())
