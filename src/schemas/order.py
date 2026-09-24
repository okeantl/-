from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0, le=10_000)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total: float
    status: str

    model_config = ConfigDict(from_attributes=True)
