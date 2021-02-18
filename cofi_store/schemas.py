from typing import List, Literal, Optional

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
