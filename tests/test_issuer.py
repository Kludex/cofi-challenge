import json
from tempfile import NamedTemporaryFile

import pytest
from pydantic import ValidationError

from cofi_store import Checkout, CheckoutIssuer
from tests.constants import VALID_JSON


def test_invalid_path():
    with pytest.raises(FileNotFoundError):
        CheckoutIssuer("potato")


@pytest.mark.parametrize(
    "content",
    [
        {"products": [{"code": "POTATO", "name": "potato", "price": 5.0}]},
        {"products": [{"code": "POTATO"}]},
        {"discounts": [{"code": "VOUCHER", "type": "2-per-1"}]},
    ],
)
def test_invalid_json(content):
    with pytest.raises(ValidationError):
        with NamedTemporaryFile("w+") as temp:
            temp.write(json.dumps(content))
            temp.seek(0)
            CheckoutIssuer(temp.name)


def test_issuer_creation():
    with NamedTemporaryFile("w+") as temp:
        temp.write(json.dumps(VALID_JSON))
        temp.seek(0)
        issuer = CheckoutIssuer(temp.name)
        assert isinstance(issuer.use_checkout(), Checkout)
