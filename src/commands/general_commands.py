"""General commands like help, hello, exit."""

from colorama import Fore


def help_command():
    """Display help information about available commands."""
    return (
        f"{Fore.YELLOW}Available Commands:\n"
        f"{Fore.YELLOW}add <name> <phone> {Fore.RESET}- Add a new contact\n"
        f"{Fore.YELLOW}delete <name> {Fore.RESET}- Delete contact from the book\n"
        f"{Fore.YELLOW}add-birthday <name> <birthday> {Fore.RESET}- Add birthday for a contact\n"
        f"{Fore.YELLOW}add-address <name> <address> {Fore.RESET}- Add address for a contact\n"
        f"{Fore.YELLOW}add-email <name> <email> {Fore.RESET}- Add email for a contact\n"
        f"{Fore.YELLOW}add-note <name> <note> {Fore.RESET}- Add note for a contact\n"
        f"{Fore.YELLOW}add-tag <name> <note_ID> <tag> {Fore.RESET}- Add tag for a note of a contact\n"
        f"{Fore.YELLOW}all {Fore.RESET}- Shows all contacts in the book\n"
        f"{Fore.YELLOW}change-phone <name> <old_phone> <new_phone> {Fore.RESET}- Change a phone number of contact\n"
        f"{Fore.YELLOW}change-birthday <name> <birthday> {Fore.RESET}- Change birthday of contact\n"
        f"{Fore.YELLOW}change-address <name> <old_address> -> <new_address> {Fore.RESET}- Change address of contact\n"
        f"{Fore.YELLOW}change-email <name> <email> {Fore.RESET}- Change email of contact\n"
        f"{Fore.YELLOW}show-phone <name> {Fore.RESET}- Show phones of contact\n"
        f"{Fore.YELLOW}show-birthday <name> {Fore.RESET}- Show birthday of contact\n"
        f"{Fore.YELLOW}show-birthdays-in <days> {Fore.RESET}- Show birthdays in the next <days> days\n"
        f"{Fore.YELLOW}show-address <name> {Fore.RESET}- Show address of contact\n"
        f"{Fore.YELLOW}show-email <name> {Fore.RESET}- Show email of contact\n"
        f"{Fore.YELLOW}show-notes <name> {Fore.RESET}- Show notes of contact\n"
        f"{Fore.YELLOW}show-notes-sorted <name> {Fore.RESET}- Show notes sorted by tags\n"
        f"{Fore.YELLOW}show-celebration-day {Fore.RESET}- Show contacts with birthdays for the next week\n"
        f"{Fore.YELLOW}show-birthdays-in <days> {Fore.RESET}- Show contacts with birthdays for the next amount of days\n"
        f"{Fore.YELLOW}find-notes <name> <search_text> {Fore.RESET}- Show note with specific text of contact\n"
        f"{Fore.YELLOW}find <field> <string> {Fore.RESET}- Search contacts by specific fields\n"
        f"{Fore.YELLOW}find-by-tag <name> <tag> {Fore.RESET}- Find notes of a contact by tag\n"
        f"{Fore.YELLOW}find-all-by-tag <tag> {Fore.RESET}- Find notes of all contacts by tag\n"
        f"{Fore.YELLOW}delete-phone <name> <phone> {Fore.RESET}- Delete phone number of contact\n"
        f"{Fore.YELLOW}delete-birthday <name> {Fore.RESET}- Delete birthday of contact\n"
        f"{Fore.YELLOW}delete-address <name> <address> {Fore.RESET}- Delete address of contact\n"
        f"{Fore.YELLOW}delete-note <name> <note_ID> {Fore.RESET}- Delete note with specific ID of contact\n"
        f"{Fore.YELLOW}delete-email <name> {Fore.RESET}- Delete email of contact\n"
        f"{Fore.YELLOW}remove-tag <name> <note_ID> <tag> {Fore.RESET}- Remove tag from a note\n"
    )


def hello_command():
    """Display a greeting message."""
    return f"{Fore.BLUE}How can I help you?"


def exit_command():
    """Return exit signal."""
    return "EXIT"

