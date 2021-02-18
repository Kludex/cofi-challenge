import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

from cofi_store.schemas import CheckoutConfig, Discount, Product


class Checkout:
    def __init__(self, products: Dict[str, Product], discounts: Dict[str, Discount]):
        self._products = products
        self._discounts = discounts
        self.items = defaultdict(int)
        self.subtotal = 0

    def _apply_discount(self, sku: str) -> float:
        """Applies discount on the product with code SKU, whenever possible.

        Args:
            sku (str): Stock Keeping Unit, or product code.

        Returns:
            float: Price of the product after applying the discounts.
        """
        price = self._products[sku].price
        discount = self._discounts.get(sku)
        if discount is None:
            return price
        if discount.type_ == "2-per-1" and self.items[sku] % 2 == 0:
            return 0
        if discount.type_ == "reduce":
            if self.items[sku] == discount.min_:
                return price - discount.value * discount.min_
            elif self.items[sku] > discount.min_:
                return price - discount.value
        return price

    def scan(self, sku: str) -> None:
        """Scans the SKU (Stock Keeping Unit) value and stores the current subtotal. In
        case the product with the provided code doesn't exist in the system, it will be
        ignored.

        Args:
            sku (str): Stock Keeping Unit, or product code.
        """
        if sku in self._products:
            self.items[sku] += 1
            self.subtotal += self._apply_discount(sku)

    def total(self) -> float:
        """Gets the total purchase price.

        Returns:
            float: Total purchase price.
        """
        return self.subtotal


class CheckoutIssuer:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as config_file:
            config = CheckoutConfig(**json.load(config_file))
            self.products = {prod.code: prod for prod in config.products}
            self.discounts = {disc.code: disc for disc in config.discounts}

    def use_checkout(self) -> Checkout:
        """User-friendly wrapper around `Checkout()`.

        Returns:
            Checkout: Checkout process object.
        """
        return Checkout(self.products, self.discounts)
