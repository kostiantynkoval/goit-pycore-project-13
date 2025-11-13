from .phone import Phone
from .name import Name
from .birthday import Birthday
from .note import Note
from .address import Address
from .email import Email
# from src.exeptions.email_already_exists import EmailAlreadyExistsError

class EmailFieldError(Exception):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = []
        self.addresses = []
        self.email = None

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
    
    def remove_address(self, address):
        for addr in self.addresses:
         if addr.value.lower() == address.lower():
            self.addresses.remove(addr)
            return True
        return False
    
    def remove_birthday(self, name):
        if self.name and self.birthday:
            self.birthday=None
            return True
        return False

    def edit_phone(self, phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             phone_number.value = Phone(new_phone).value
             return True
        return False
    
    def edit_address(self, addr, new_addr):
        for ad in self.addresses:
            if ad.value == addr:
             ad.value = Address(new_addr).value
             return True
        return False

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
             return phone_number
        return None

    def add_email(self, email):
        if not self.email:
            self.email = Email(email)
            return True
        else:
            raise EmailFieldError("There is already an email for this contact. Please use change-email command to update it.")

    def edit_email(self, new_email):
        if self.email:
            self.email = Email(new_email)
            return True
        else:
            raise EmailFieldError("There is no email for this contact. Please use add-email command to add one.")

    def delete_email(self):
        if self.email:
            self.email = None
            return True
        else:
            raise EmailFieldError("There is no email for this contact. Please use add-email command to add one.")

    def add_note(self, content: str):
        note = Note(content)
        self.notes.append(note)
        return note

    def find_note_by_id(self, note_id: str):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def find_notes(self, search_text: str):
        return [note for note in self.notes if note.matches_search(search_text)]

    def edit_note(self, note_id: str, new_content: str):
        note = self.find_note_by_id(note_id)
        if note:
            note.edit(new_content)
            return True
        return False

    def delete_note(self, note_id: str):
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            return True
        return False

    def show_all_notes(self):
        return self.notes

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        notes_count = f", notes: {len(self.notes)}" if self.notes else ""
        phones_str = "; ".join(p.value for p in self.phones)
        address_str = "; ".join(a.value for a in self.addresses) if self.addresses else "N/A"
        email_str = f", email: {self.email.value}" if self.email else ""
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"birthday: {birthday_str}, "
            f"address: {address_str}"
            f"{notes_count}"
            f"{email_str}"
        )