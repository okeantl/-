from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)
