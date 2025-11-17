"""Command registry - single entry point for all commands."""

from colorama import Fore
from commands.contact_commands import add_contact, delete_contact, find, get_all_contacts
from commands.phone_commands import update_contact, get_contact, delete_phone
from commands.address_commands import add_address, get_address, update_address, delete_address
from commands.birthday_commands import (
    add_birthday, get_birthday, update_birthday, 
    delete_birthday, birthdays, birthdays_in_range
)
from commands.note_commands import (
    add_note, show_notes, find_notes, edit_note, delete_note,
    add_tag, remove_tag, find_by_tag, find_all_by_tag, show_notes_sorted
)
from commands.email_commands import add_email, update_email, show_email, delete_email
from commands.general_commands import help_command, hello_command, exit_command


# Command mapping dictionary - single source of truth for all commands
COMMANDS = {
    # General commands
    "close": lambda args, book: exit_command(),
    "exit": lambda args, book: exit_command(),
    "hello": lambda args, book: hello_command(),
    "help": lambda args, book: help_command(),
    
    # Contact commands
    "add": add_contact,
    "delete": delete_contact,
    "find": find,
    "all": lambda args, book: get_all_contacts(book),
    
    # Phone commands
    "change-phone": update_contact,
    "show-phone": get_contact,
    "delete-phone": delete_phone,
    
    # Address commands
    "add-address": add_address,
    "show-address": get_address,
    "change-address": update_address,
    "delete-address": delete_address,
    
    # Birthday commands
    "add-birthday": add_birthday,
    "show-birthday": get_birthday,
    "change-birthday": update_birthday,
    "delete-birthday": delete_birthday,
    "birthdays": lambda args, book: birthdays(book),
    "show-birthdays-in": birthdays_in_range,
    "show-celebration-day": lambda args, book: birthdays(book),
    
    # Note commands
    "add-note": add_note,
    "show-notes": show_notes,
    "find-notes": find_notes,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "add-tag": add_tag,
    "remove-tag": remove_tag,
    "find-by-tag": find_by_tag,
    "find-all-by-tag": find_all_by_tag,
    "show-notes-sorted": show_notes_sorted,
    
    # Email commands
    "add-email": add_email,
    "change-email": update_email,
    "show-email": show_email,
    "delete-email": delete_email,
}


def execute_command(command, args, book):
    """
    Execute a command based on the command name.
    
    Args:
        command: The command name
        args: Arguments for the command
        book: The AddressBook instance
        
    Returns:
        The result of the command execution or None if command not found
    """
    handler = COMMANDS.get(command)
    if handler:
        return handler(args, book)
    return None


def get_all_commands():
    """Return a list of all available command names."""
    return list(COMMANDS.keys())

