# -*- coding: utf-8 -*-
from functools import wraps


def update_quality_and_sell_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if item := kwargs.get("item"):
            check_quality(i=item)
        func(*args, **kwargs)
        if item:
            check_quality(i=item)
            item.sell_in -= 1

    def check_quality(i: "Item") -> None:
        i.quality = 50 if i.quality > 50 else i.quality
        i.quality = 0 if i.quality < 0 else i.quality

    return wrapper


class GildedTros:
    OPERATIONS = {
        "LegendaryItem": "update_for_legendary_item",
        "SmellyItem": "update_for_smelly_item",
        "GoodWine": "update_for_good_wine",
        "BackstagePass": "update_for_backstage_pass"
    }

    def __init__(self, items: list["Item"]) -> None:
        self.items = items

    def update_items(self) -> None:
        for item in self.items:
            method_name = "update_default"
            for cls in item.__class__.__mro__:
                if name := self.OPERATIONS.get(cls.__name__):
                    method_name = name
                    break
            method = getattr(self, method_name)
            method(item=item)

    @update_quality_and_sell_in
    def update_default(self, item: "Item") -> None:
        degradation = self._calculate_degrade(item=item)
        item.quality += degradation

    @staticmethod
    def update_for_legendary_item(item: "Item") -> None:
        item.quality = 80

    @update_quality_and_sell_in
    def update_for_smelly_item(self, item: "Item") -> None:
        degradation = self._calculate_degrade(item=item, degrade=-2)
        item.quality += degradation

    @update_quality_and_sell_in
    def update_for_good_wine(self, item: "Item") -> None:
        increase = 2 if item.sell_in < 1 else 1
        item.quality += increase

    @update_quality_and_sell_in
    def update_for_backstage_pass(self, item: "Item") -> None:
        if item.sell_in < 1:
            item.quality = 0
        else:
            item.quality += 1
            if item.sell_in < 11:
                item.quality += 1
            if item.sell_in < 6:
                item.quality += 1

    @staticmethod
    def _calculate_degrade(item: "Item", degrade: int = -1) -> int:
        if item.sell_in < 1:
            degrade *= 2
        return degrade


class Item:
    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class SmellyItem(Item):
    pass


class LegendaryItem(Item):
    pass


class GoodWine(Item):
    pass


class BackstagePass(Item):
    pass
