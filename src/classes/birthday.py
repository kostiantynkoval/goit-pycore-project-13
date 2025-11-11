from datetime import datetime
from .field import Field

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")