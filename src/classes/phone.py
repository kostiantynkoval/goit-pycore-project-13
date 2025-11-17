from classes.field import Field

class Phone(Field):
    def __init__(self, value):
     if len(value) != 10 or not value.isdigit():
         raise ValueError("Phone number must be 10 digits")
     super().__init__(value)