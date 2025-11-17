from commands.contact_commands import add_contact, delete_contact, find, get_all_contacts
from commands.phone_commands import update_contact, get_contact, delete_phone
from commands.address_commands import add_address, get_address, update_address, delete_address
from commands.birthday_commands import add_birthday, get_birthday, update_birthday, delete_birthday, birthdays, birthdays_in_range
from commands.note_commands import add_note, show_notes, find_notes, edit_note, delete_note, add_tag, remove_tag, find_by_tag, find_all_by_tag, show_notes_sorted
from commands.email_commands import add_email, update_email, show_email, delete_email
from commands.general_commands import help_command, hello_command, exit_command

__all__ = [
    # Contact commands
    'add_contact', 'delete_contact', 'find', 'get_all_contacts',
    # Phone commands
    'update_contact', 'get_contact', 'delete_phone',
    # Address commands
    'add_address', 'get_address', 'update_address', 'delete_address',
    # Birthday commands
    'add_birthday', 'get_birthday', 'update_birthday', 'delete_birthday', 'birthdays', 'birthdays_in_range',
    # Note commands
    'add_note', 'show_notes', 'find_notes', 'edit_note', 'delete_note', 
    'add_tag', 'remove_tag', 'find_by_tag', 'find_all_by_tag', 'show_notes_sorted',
    # Email commands
    'add_email', 'update_email', 'show_email', 'delete_email',
    # General commands
    'help_command', 'hello_command', 'exit_command',
]

