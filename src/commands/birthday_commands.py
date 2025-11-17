"""Commands for managing birthdays."""

from colorama import Fore
from classes.address_book import AddressBook
from exceptions import (
    ContactNotFoundError,
    BirthdayNotFoundError,
    InsufficientArgumentsError,
)
from commands.decorators import input_error


@input_error
def add_birthday(args, book: AddressBook):
    """Add a birthday to a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-birthday <name> <birthday>")
    
    name, birthday = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.add_birthday(birthday)
    return f"{Fore.GREEN}Birthday added"


@input_error
def get_birthday(args, book: AddressBook):
    """Show birthday for a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-birthday <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    birthday_str = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A"
    lines = [
        f"{Fore.MAGENTA}Contact name: {record.name.value}",
        f"Birthday: {birthday_str}",
        "-----------------------"
    ]
    return "\n".join(lines)


@input_error
def update_birthday(args, book: AddressBook):
    """Update a birthday for a contact."""
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: change-birthday <name> <birthday>")
    
    name, new_bday = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if not record.edit_birthday(new_bday):
        raise BirthdayNotFoundError(f"Contact '{name}' has no birthday to update")
    
    return f"{Fore.GREEN}Birthday is updated"


@input_error
def delete_birthday(args, book: AddressBook):
    """Delete a birthday from a contact."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: delete-birthday <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if not record.remove_birthday(name):
        raise BirthdayNotFoundError(f"Contact '{name}' has no birthday date")
    
    return f"{Fore.GREEN}Birthday of contact {name} deleted successfully"


@input_error
def birthdays(book: AddressBook):
    """Show upcoming birthdays for the next week."""
    if not book:
        raise ContactNotFoundError("Address book is empty")
    
    birthdays_list = book.get_upcoming_birthdays()
    if not birthdays_list:
        return f"{Fore.YELLOW}No upcoming birthdays"
    
    lines = []
    for b in birthdays_list:
        lines.append(
            f"{Fore.MAGENTA}Contact name: {b['name']}\n"
            f"Celebration day: {b['congratulation_date']}\n"
            "-----------------------"
        )
    return "\n".join(lines)


@input_error
def birthdays_in_range(args, book: AddressBook):
    """Show birthdays in a specified number of days."""
    if len(args) < 1:
        raise InsufficientArgumentsError("Provide a range of birthdays")
    try:
        days = int(args[0])
    except ValueError:
        raise ValueError("Days must be an integer number")
    birthdays_list = book.get_birthdays_in_range(days)
    if not birthdays_list:
        return f"{Fore.YELLOW}No birthdays in the next {days} days"
    lines = []
    for b in birthdays_list:
        lines.append(
            f"{Fore.MAGENTA}Contact: {b['name']}\n"
            f"Birthday: {b['birthday']}\n"
            "-----------------------"
        )
    return "\n".join(lines)

