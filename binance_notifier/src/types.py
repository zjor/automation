from pydantic import BaseModel


class BinanceOrder(BaseModel):
    orderId: int
    clientOrderId: str
    symbol: str
    side: str
    status: str
    price: str
    origQty: str
