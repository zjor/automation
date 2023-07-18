from pydantic import BaseModel, Field


class BinanceOrder(BaseModel):
    orderId: int
    clientOrderId: str
    symbol: str
    type_: str = Field(..., alias='type')
    side: str
    status: str
    price: str
    origQty: str
