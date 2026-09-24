class Cart:
    def __init__(self):
        self.items = []  # список (название, цена)

    def __add__(self, item):
        new_cart = Cart()
        new_cart.items = self.items.copy()
        new_cart.items.append(item)
        return new_cart

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __call__(self):
        return sum(price for _, price in self.items)


cart = Cart()
cart = cart + ("Ноутбук", 75000)
cart = cart + ("Мышь", 1200)
cart = cart + ("Клавиатура", 3500)

print(len(cart))
print(cart[0][0])
for name, price in cart:
    print(f"{name}: {price}")
print(cart())
