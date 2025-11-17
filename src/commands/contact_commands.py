"""Commands for managing contacts."""

from colorama import Fore
from classes.address_book import AddressBook
from classes.record import Record
from exceptions import (
    ContactNotFoundError,
    InsufficientArgumentsError,
    PhoneAlreadyExistsError,
)
from commands.decorators import input_error


@input_error
def add_contact(args, book: AddressBook):
    """Add a new contact or update existing contact with a phone number."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add <name> <phone>")
    
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"{Fore.GREEN}Contact added"
    if phone:
        if any(phone == p.value for p in record.phones):
            raise PhoneAlreadyExistsError("This phone number already exists.")
        record.add_phone(phone)
        message = f"{Fore.GREEN}Contact updated"
    return message


@input_error
def delete_contact(args, book: AddressBook):
    """Delete a contact from the address book."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: delete <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    confirmation = input(f"{Fore.YELLOW}Are you sure? You are going to delete the entire contact '{name}'? (yes/no):")
    if confirmation.strip().lower() != "yes":
        return f"{Fore.CYAN} Deletion cancelled."
    
    if book.delete(name):
        return f"{Fore.GREEN}Contact {name} deleted successfully"
    else:
        raise ContactNotFoundError(f"Contact '{name}' not found")


@input_error
def find(args, book: AddressBook):
    """Find contacts by field and string."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: find <field> <string>")
    
    field = args[0]
    string = args[1]
    lines = []
    records = book.find_by_any_arg(field, string)

    if len(records) == 0:
        raise ContactNotFoundError(f"Contacts with the field {field} that contain {string} not found.")
    
    for r in records:
        lines.append(str(r))
    return "\n".join(lines)


@input_error
def get_all_contacts(book: AddressBook):
    """Get all contacts from the address book."""
    if not book:
        return f"{Fore.YELLOW}Address book is empty"
    lines = []
    for record in book.data.values():
        phones_str = "; ".join(p.value for p in record.phones) if record.phones else "N/A"
        birthday_str = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A"
        address_str = "; ".join(a.value for a in record.addresses) if record.addresses else "N/A"
        email_str = f"{record.email.value}" if record.email else "N/A"
        notes_count = f"{len(record.notes)}" if record.notes else "N/A"

        lines.append(
            f"{Fore.MAGENTA}Contact name: {record.name.value}\n"
            f"Phones: {phones_str}\n"
            f"Birthday: {birthday_str}\n"
            f"Address: {address_str}\n"
            f"Email: {email_str}\n"
            f"Notes: {notes_count}\n"
            "-----------------------"
        )
    return "\n".join(lines)

