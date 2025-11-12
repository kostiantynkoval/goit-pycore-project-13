from .phone import Phone
from .name import Name
from .birthday import Birthday
from .address import Address

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.addresses = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_address(self, address):
        self.addresses.append(Address(address))

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
        phones_str = "; ".join(p.value for p in self.phones)
        address_str = "; ".join(a.value for a in self.addresses) if self.addresses else "N/A"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"birthday: {birthday_str}, "
            f"address: {address_str}"
        )
