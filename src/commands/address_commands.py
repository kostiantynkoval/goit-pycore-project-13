"""Commands for managing addresses."""

from colorama import Fore
from classes.address_book import AddressBook
from exceptions import (
    ContactNotFoundError,
    AddressNotFoundError,
    InsufficientArgumentsError,
)
from commands.decorators import input_error


@input_error
def add_address(args, book: AddressBook):
    """Add an address to a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-address <name> <address>")
    
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.add_address(address)
    return f"{Fore.GREEN}Address added"


@input_error
def get_address(args, book: AddressBook):
    """Show addresses for a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-address <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    address_str = "; ".join(a.value for a in record.addresses) if record.addresses else "N/A"
    lines = [
        f"{Fore.MAGENTA}Contact name: {record.name.value}",
        f"Address: {address_str}",
        "-----------------------"
    ]
    return "\n".join(lines)


@input_error
def update_address(args, book: AddressBook):
    """Update an address for a contact."""
    if len(args) < 3:
        raise InsufficientArgumentsError("Usage: change-address <name> <old_address> -> <new_address>")
    
    name = args[0]
    rest = " ".join(args[1:])
    try:
        old_addr, new_addr = rest.split("->")
        old_addr = old_addr.strip().replace("\r", "")
        new_addr = new_addr.strip().replace("\r", "")
    except ValueError:
        raise ValueError("Please separate old and new addresses with '->'")
    
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if old_addr.lower() not in [a.value.lower() for a in record.addresses]:
        raise AddressNotFoundError(f"Contact {name} has no address {old_addr}")
    
    if not record.edit_address(old_addr, new_addr):
        raise AddressNotFoundError(f"Contact {name} has no address {old_addr}")
    
    return f"{Fore.GREEN}Address of the contact {name} updated"


@input_error
def delete_address(args, book: AddressBook):
    """Delete an address from a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: delete-address <name> <address>")
    
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if not record.remove_address(address):
        raise AddressNotFoundError(f"Address '{address}' not found")
    
    return f"{Fore.GREEN}Address {address} of contact {name} deleted successfully"

