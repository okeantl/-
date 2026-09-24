import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User:
    def __init__(self, name, email):
        self.name = name
        if not EMAIL_PATTERN.match(email):
            raise ValueError("Неверный формат email")
        self.email = email

    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self.email
