"""Commands for managing phone numbers."""

from colorama import Fore
from classes.address_book import AddressBook
from exceptions import (
    ContactNotFoundError,
    PhoneNotFoundError,
    InsufficientArgumentsError,
    MinimumPhoneRequiredError,
)
from commands.decorators import input_error


@input_error
def update_contact(args, book: AddressBook):
    """Update a phone number for a contact."""
    if len(args) < 3:
        raise InsufficientArgumentsError("Usage: change-phone <name> <old_phone> <new_phone>")
    
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if not record.edit_phone(old_phone, new_phone):
        raise PhoneNotFoundError(f"Phone number '{old_phone}' not found for contact '{name}'")
    
    return f"{Fore.GREEN}Phone updated"


@input_error
def get_contact(args, book: AddressBook):
    """Show phone numbers for a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-phone <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    phones_str = "; ".join(p.value for p in record.phones) if record.phones else "N/A"
    lines = [
        f"{Fore.MAGENTA}Contact name: {record.name.value}",
        f"Phones: {phones_str}",
        "-----------------------"
    ]
    return "\n".join(lines)


@input_error
def delete_phone(args, book: AddressBook):
    """Delete a phone number from a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: delete-phone <name> <phone>")

    name = args[0]
    phone = args[1]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if len(record.phones) <= 1:
        raise MinimumPhoneRequiredError("Contact must have at least one phone number.")
    
    if not record.remove_phone(phone):
        raise PhoneNotFoundError(f"Phone number '{phone}' not found")
    
    return f"{Fore.GREEN}Phone number {phone} of contact {name} deleted successfully"

