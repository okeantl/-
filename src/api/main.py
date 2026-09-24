import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.api import auth
from src.api.limiter import limiter
from src.api.routes import background, orders, products

load_dotenv()

# Домены фронтенда, которым разрешены запросы к API
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000",
    ).split(",")


class OrderCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название товара")
    price: float = Field(..., gt=0, description="Цена товара (должна быть больше 0)")
    quantity: int = Field(..., ge=0, description="Количество на складе")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Название не может быть пустым")
        return v.strip()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    )
# Лимитер и обработчик ошибки 429 Too Many Requests
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
    )

# Товары пока живут в памяти: POST, PUT и DELETE меняют этот список
products_data = [
    {"id": 1, "name": "Ноутбук", "price": 50000, "quantity": 10},
    {"id": 2, "name": "Мышь", "price": 1500, "quantity": 20},
    {"id": 3, "name": "Клавиатура", "price": 3000, "quantity": 15}
    ]


def find_product(product_id: int) -> dict:
    """Найти товар по ID или ответить 404 Not Found"""
    for product in products_data:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Товар с ID {product_id} не найден"
        )

# GET - список товаров (200 OK)
@app.get("/products")
@limiter.limit(os.getenv("RATE_LIMIT_PRODUCTS", "30/minute"))
def get_products(request: Request):
    return products_data

# GET - товар по ID (200 OK или 404 Not Found)
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return find_product(product_id)

# POST - создание товара (201 Created; неверные данные отклоняет ProductCreate - 422)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    new_id = max((p["id"] for p in products_data), default=0) + 1
    new_product = {"id": new_id, **product.model_dump()}
    products_data.append(new_product)
    return new_product

# PUT - полное обновление товара (200 OK или 404 Not Found)
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate):
    existing = find_product(product_id)
    existing.update(product.model_dump())
    return existing

# DELETE - удаление товара (204 No Content или 404 Not Found)
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    products_data.remove(find_product(product_id))

@app.post("/orders")
def create_order(order: OrderCreate):
    # В реальном приложении здесь будет создание заказа в БД
    return {
        "id": 5,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "message": "Заказ создан"
        }


# Роутер регистрации и входа: POST /register, POST /login
app.include_router(auth.router)

# Слоистые роутеры: GET /api/v1/products/{id}, POST /api/v1/orders/, POST /api/v1/orders/{id}/cancel, GET /api/v1/orders/{id}
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")

# Роутер фоновых задач: POST /orders/{order_id}/confirm, POST /exports, GET /exports/{task_id}, POST /orders/background
app.include_router(background.router)
