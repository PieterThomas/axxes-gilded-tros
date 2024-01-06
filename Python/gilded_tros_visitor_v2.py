# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from functools import wraps


def update_quality_and_sell_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        item = None
        if len(args) == 1:
            item = args[0]
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
    def __init__(self, items: list["Item"]) -> None:
        self.items = items

    def update_items(self) -> None:
        for item in self.items:
            item.update()


class Item(ABC):
    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    @abstractmethod
    def update(self) -> None:
        pass


class NormalItem(Item):
    @update_quality_and_sell_in
    def update(self) -> None:
        degradation = -2 if self.sell_in < 1 else -1
        self.quality += degradation


class SmellyItem(Item):
    @update_quality_and_sell_in
    def update(self) -> None:
        degradation = -4 if self.sell_in < 1 else -2
        self.quality += degradation


class LegendaryItem(Item):
    def update(self) -> None:
        self.quality = 80


class GoodWine(Item):
    @update_quality_and_sell_in
    def update(self) -> None:
        increase = 2 if self.sell_in < 1 else 1
        self.quality += increase


class BackstagePass(Item):
    @update_quality_and_sell_in
    def update(self) -> None:
        if self.sell_in < 1:
            self.quality = 0
        else:
            self.quality += 1
            if self.sell_in < 11:
                self.quality += 1
            if self.sell_in < 6:
                self.quality += 1
