import re

EMAIL_REGEXP = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

class Email:
    def __init__(self, value):
        try:
            if EMAIL_REGEXP.match(value):
                super().__init__(value)
        except ValueError:
            raise ValueError("Invalid email format. Please enter a valid email address.")