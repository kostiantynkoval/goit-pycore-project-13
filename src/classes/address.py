from .field import Field

class Address(Field):
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Address cannot be empty")
        super().__init__(value)