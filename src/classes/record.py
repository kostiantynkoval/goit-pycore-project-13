from .phone import Phone
from .name import Name
from .birthday import Birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        for phone_number in self.phones:
         if phone_number.value == phone:
            self.phones.remove(phone_number)
            return True
        return False

    def edit_phone(self, phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             phone_number.value = Phone(new_phone).value
             return True
        return False

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             return phone_number
        return None

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"
