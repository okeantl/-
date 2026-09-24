import requests

# Тело заказа SFMShop, которое отправим на сервер.
order = {"user_id": 1, "product_id": 2, "quantity": 1}

# POST создаёт ресурс, тело передаём параметром json — requests сериализует его сам.
response_post = requests.post("https://httpbin.org/post", json=order)

# PUT обновляет ресурс целиком, тело передаём тем же способом.
response_put = requests.put("https://httpbin.org/put", json=order)

# DELETE удаляет ресурс, тело для него не нужно.
response_delete = requests.delete("https://httpbin.org/delete")

# GET на несуществующий путь — сервер отвечает статусом 404.
response_missing = requests.get("https://httpbin.org/nonexistent")

# GET на адрес, который принимает только POST, — сервер отвечает статусом 405.
response_wrong_method = requests.get("https://httpbin.org/post")

# httpbin возвращает тело POST-запроса обратно в поле json — проверим, что сервер принял заказ.
echoed_order = response_post.json()["json"]

print(f"POST /post -> {response_post.status_code}, сервер принял тело: {echoed_order}")
print(f"PUT /put -> {response_put.status_code}")
print(f"DELETE /delete -> {response_delete.status_code}")
print(f"GET /nonexistent -> {response_missing.status_code} (ресурс не найден)")
print(f"GET /post -> {response_wrong_method.status_code} (метод не разрешён для этого адреса)")
