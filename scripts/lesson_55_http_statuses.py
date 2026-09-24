from http import HTTPStatus


class ProductAPI:
    """Мини-роутер SFMShop: хранит товары в памяти и отвечает
    правильным HTTP-методом и статусом, как настоящий REST API."""

    def __init__(self):
        self._products = {}   # id -> {"name": str, "price": float}
        self._next_id = 1

    def handle(self, method, product_id=None, body=None):
        """Возвращает кортеж (status_code, payload).
        payload - dict или None (для 204)."""
        if method == "GET":
            if product_id is None:
                return HTTPStatus.OK, {"products": list(self._products.values())}
            product = self._products.get(product_id)
            if product is None:
                return HTTPStatus.NOT_FOUND, {"error": f"товар {product_id} не найден"}
            return HTTPStatus.OK, {"product": product}

        if method == "POST":
            if body is None or body.get("price", 0) < 0:
                return HTTPStatus.BAD_REQUEST, {"error": "цена не может быть отрицательной"}
            new_id = self._next_id
            self._next_id += 1
            self._products[new_id] = {"name": body["name"], "price": body["price"]}
            return HTTPStatus.CREATED, {"id": new_id, "status": "created"}

        if method == "PUT":
            if product_id not in self._products:
                return HTTPStatus.NOT_FOUND, {"error": f"товар {product_id} не найден"}
            self._products[product_id] = {"name": body["name"], "price": body["price"]}
            return HTTPStatus.OK, {"id": product_id, "status": "updated"}

        if method == "DELETE":
            if product_id not in self._products:
                return HTTPStatus.NOT_FOUND, {"error": f"товар {product_id} не найден"}
            del self._products[product_id]
            return HTTPStatus.NO_CONTENT, None

        return HTTPStatus.METHOD_NOT_ALLOWED, {"error": f"метод {method} не поддерживается"}


def show(label, result):
    status, payload = result
    print(f"{label}: {status.value} {status.phrase} -> {payload}")


api = ProductAPI()

show("POST новый товар", api.handle("POST", body={"name": "Худи SFM", "price": 3990}))
show("POST с ценой < 0", api.handle("POST", body={"name": "Кепка", "price": -100}))
show("GET список", api.handle("GET"))
show("GET товар 1", api.handle("GET", product_id=1))
show("GET товар 99", api.handle("GET", product_id=99))
show("PUT товар 1", api.handle("PUT", product_id=1, body={"name": "Худи SFM", "price": 4490}))
show("PUT товар 99", api.handle("PUT", product_id=99, body={"name": "X", "price": 10}))
show("DELETE товар 1", api.handle("DELETE", product_id=1))
show("DELETE товар 1 снова", api.handle("DELETE", product_id=1))
show("PATCH товар 1", api.handle("PATCH", product_id=1))
