import json
from tempfile import NamedTemporaryFile

import pytest

from cofi_store import Checkout, CheckoutIssuer
from tests.constants import VALID_JSON


def get_checkout(content: dict = VALID_JSON):
    with NamedTemporaryFile("w+") as temp:
        temp.write(json.dumps(content))
        temp.seek(0)
        issuer = CheckoutIssuer(temp.name)
        return issuer.use_checkout()


def test_scan_invalid_code():
    checkout = get_checkout()
    checkout.scan("POTATO")
    assert checkout.total() == 0


@pytest.mark.parametrize(
    "products,total",
    [
        (["VOUCHER", "VOUCHER", "TSHIRT", "MUG"], 32.5),
        (["TSHIRT", "TSHIRT", "TSHIRT", "TSHIRT"], 76),
    ],
)
def test_discounts(products, total):
    checkout = get_checkout()
    for product in products:
        checkout.scan(product)
    assert checkout.total() == total


@pytest.mark.parametrize(
    "content,products,total",
    [
        (
            {
                "products": [
                    {"code": "VOUCHER", "name": "Cofi Voucher", "price": 5.0},
                    {"code": "TSHIRT", "name": "Cofi T-Shirt", "price": 20.0},
                    {"code": "MUG", "name": "Cofi Coffee Mug", "price": 7.5},
                ],
                "discounts": [
                    {"code": "VOUCHER", "type": "2-per-1"},
                    {"code": "VOUCHER", "type": "reduce", "min": "3", "value": 1.0},
                ],
            },
            ["VOUCHER", "VOUCHER", "VOUCHER"],
            12,
        )
    ],
)
def test_multiple_discounts(content, products, total):
    checkout = get_checkout(content)
    for product in products:
        checkout.scan(product)
        print(checkout.subtotal)
    assert checkout.total() == total
