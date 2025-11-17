"""Commands for managing emails."""

from colorama import Fore
from classes.address_book import AddressBook
from exceptions import (
    ContactNotFoundError,
    InsufficientArgumentsError,
)
from commands.decorators import input_error


@input_error
def add_email(args, book: AddressBook):
    """Add an email to a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-email <name> <email>")
    
    name, email = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    record.add_email(email)
    return f"{Fore.GREEN}Email is added"


@input_error
def update_email(args, book: AddressBook):
    """Update an email for a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: change-email <name> <email>")
    
    name, new_email = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.edit_email(new_email)
    return f"{Fore.GREEN}Email is updated"


@input_error    
def show_email(args, book: AddressBook):
    """Show email for a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-email <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    lines = [
        f"{Fore.MAGENTA}Contact name: {record.name.value}",
        f"Email: {record.email.value if record.email else 'N/A'}",
        "-----------------------"
    ]
    return "\n".join(lines)


@input_error
def delete_email(args, book: AddressBook):
    """Delete an email from a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: delete-email <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.delete_email()
    return f"{Fore.GREEN}Email is removed"

