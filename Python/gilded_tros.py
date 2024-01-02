# -*- coding: utf-8 -*-

class GildedTros:
    _backstage_pass_names = ["Backstage passes for Re:Factor", "Backstage passes for HAXX"]
    _good_wine_name = "Good Wine"
    _legendary_item_name = "B-DAWG Keychain"
    _smelly_item_names = ["Duplicate Code", "Long Methods", "Ugly Variable Names"]

    def __init__(self, items: list["Item"]) -> None:
        self.items = items

    def update_items(self) -> None:
        for item in self.items:
            if item.name == self._legendary_item_name:
                continue
            self._update_quality(item=item)
            self._update_sell_in(item=item)

    def _update_quality(self, item: "Item") -> None:
        is_expired = item.sell_in < 1

        if item.name == self._good_wine_name:
            increase = 2 if is_expired else 1
            item.quality += increase
        elif item.name in self._backstage_pass_names:
            if is_expired:
                item.quality = 0
            else:
                item.quality += 1
                if item.sell_in < 11:
                    item.quality += 1
                if item.sell_in < 6:
                    item.quality += 1
        else:
            degrade = self._calculate_degrade(item=item, is_expired=is_expired)
            item.quality += degrade

        item.quality = 50 if item.quality > 50 else item.quality
        item.quality = 0 if item.quality < 0 else item.quality

    @staticmethod
    def _update_sell_in(item: "Item") -> None:
        item.sell_in -= 1

    def _calculate_degrade(self, item: "Item", is_expired: bool) -> int:
        degrade = -1
        if item.name in self._smelly_item_names:
            degrade *= 2
        if is_expired:
            degrade *= 2
        return degrade


class Item:
    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
