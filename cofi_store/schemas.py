from typing import List, Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from pydantic import BaseModel, Field, PositiveFloat


class Product(BaseModel):
    code: str
    name: str
    price: PositiveFloat


class Discount(BaseModel):
    code: str
    type_: Literal["2-per-1", "reduce"] = Field(..., alias="type")
    min_: Optional[int] = Field(None, alias="min")
    value: Optional[float] = None


class CheckoutConfig(BaseModel):
    products: List[Product]
    discounts: List[Discount]
