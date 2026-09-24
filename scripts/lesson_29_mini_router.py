import json


class MiniRouter:
    def __init__(self):
        # routes: ключ (method, path_pattern) -> функция-обработчик
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def dispatch(self, method, path):
        # 1) точное совпадение пути (например, GET /products)
        handler = self.routes.get((method, path))
        if handler is not None:
            return handler()
        # 2) совпадение с параметром пути /products/{product_id}
        for (m, pattern), h in self.routes.items():
            if m != method or "{" not in pattern:
                continue
            pat_parts = pattern.split("/")
            req_parts = path.split("/")
            if len(pat_parts) != len(req_parts):
                continue
            params = {}
            matched = True
            for pp, rp in zip(pat_parts, req_parts):
                if pp.startswith("{") and pp.endswith("}"):
                    params[pp[1:-1]] = rp
                elif pp != rp:
                    matched = False
                    break
            if matched:
                return h(**params)
        # 3) ничего не подошло
        return 404, {"error": "Not Found"}


PRODUCTS = {
    1: {"id": 1, "name": "Ноутбук", "price": 50000},
    2: {"id": 2, "name": "Мышь", "price": 1500},
    3: {"id": 3, "name": "Клавиатура", "price": 3000},
}


def get_products():
    return 200, list(PRODUCTS.values())


def get_product(product_id):
    pid = int(product_id)
    product = PRODUCTS.get(pid)
    if product is None:
        return 404, {"error": "Товар не найден"}
    return 200, product


router = MiniRouter()
router.add_route("GET", "/products", get_products)
router.add_route("GET", "/products/{product_id}", get_product)


def make_response(method, path):
    status, body = router.dispatch(method, path)
    return f"{status} {json.dumps(body, ensure_ascii=False)}"


requests = [
    ("GET", "/products"),
    ("GET", "/products/2"),
    ("GET", "/products/99"),
    ("POST", "/products"),
]
for method, path in requests:
    print(f"{method} {path} -> {make_response(method, path)}")
