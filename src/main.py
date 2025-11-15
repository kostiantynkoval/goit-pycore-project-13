from colorama import Fore, init
from data_storage import save_data, load_data
from classes.address_book import AddressBook
from classes.record import Record, EmailFieldError
from exceptions import (
    ContactNotFoundError,
    PhoneNotFoundError,
    AddressNotFoundError,
    BirthdayNotFoundError,
    NoteNotFoundError,
    InsufficientArgumentsError,
    MinimumPhoneRequiredError,
    PhoneAlreadyExistsError,
)

init(autoreset=True)


def parse_input(user_input):
    commands = user_input.split()
    if not commands:
        return "", []
    cmd, *args = commands
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ContactNotFoundError as e:
            return f"{Fore.RED}{str(e) if str(e) else 'Contact not found'}"
        except PhoneNotFoundError as e:
            return f"{Fore.RED}{str(e) if str(e) else 'Phone number not found'}"
        except PhoneAlreadyExistsError as e:
            return f"{Fore.YELLOW}{str(e) if str(e) else 'This phone number already exists.'}"
        except AddressNotFoundError as e:
            return f"{Fore.RED}{str(e) if str(e) else 'Address not found'}"
        except BirthdayNotFoundError as e:
            return f"{Fore.RED}{str(e) if str(e) else 'Birthday not found'}"
        except NoteNotFoundError as e:
            return f"{Fore.RED}{str(e) if str(e) else 'Note not found'}"
        except InsufficientArgumentsError as e:
            return f"{Fore.RED}{str(e)}"
        except MinimumPhoneRequiredError as e:
            return f"{Fore.RED}{str(e)}"
        except EmailFieldError as e:
            return f"{Fore.RED}{str(e)}"
        except ValueError as e:
            return f"{Fore.RED}{str(e)}"
        except (IndexError, KeyError) as e:
            return f"{Fore.RED}Invalid arguments provided"

    return inner

# ****** Start Manipulations with contact ******
@input_error
def add_contact(args, book: AddressBook):
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
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: delete <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    confirmation=input(f"{Fore.YELLOW}Are you sure? You are going to delete the entire contact '{name}'? (yes/no):")
    if confirmation.strip().lower()!="yes":
        return f"{Fore.CYAN} Deletion cancelled."
    
    if book.delete(name):
        return f"{Fore.GREEN}Contact {name} deleted successfully"
    else:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    
@input_error
def find(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: find <field> <string>")
    
    field = args[0]
    string = args[1]
    lines=[]
    records = book.find_by_any_arg(field, string)

    if len(records) == 0:
        raise ContactNotFoundError(f"Contacts with the field {field} that contain {string} not found.")
    
    for r in records:
        lines.append(str(r))
    return "\n".join(lines)

@input_error
def get_all_contacts(book: AddressBook):
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
# ****** End Manipulations with contact ******


# ****** Start Manipulations with phone ******
@input_error
def update_contact(args, book: AddressBook):
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
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: delete-phone <name> <phone>")

    name = args[0]
    phone=args[1]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if len(record.phones) <=1:
        raise MinimumPhoneRequiredError("Contact must have at least one phone number.")
    
    if not record.remove_phone(phone):
        raise PhoneNotFoundError(f"Phone number '{phone}' not found")
    
    return f"{Fore.GREEN}Phone number {phone} of contact {name} deleted successfully"
# ****** End Manipulations with phone ******


# ****** Start Manipulations with address ******
@input_error
def add_address(args, book:AddressBook):
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
    if len(args) < 3:
        raise InsufficientArgumentsError("Usage: change-address <name> <old_address> -> <new_address>")
    
    name=args[0]
    rest=" ".join(args[1:])
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
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: delete-address <name> <address>")
    
    name = args[0]
    address=" ".join(args[1:])
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    if not record.remove_address(address):
        raise AddressNotFoundError(f"Address '{address}' not found")
    
    return f"{Fore.GREEN}Address {address} of contact {name} deleted successfully"
# ****** End Manipulations with address ******


# ****** Start Manipulations with birthday ******
@input_error
def add_birthday(args, book:AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-birthday <name> <birthday>")
    
    name, birthday = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.add_birthday(birthday)
    return f"{Fore.GREEN}Birthday added"

@input_error
def get_birthday(args, book:AddressBook):
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
def birthdays(book:AddressBook):
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

# ****** End Manipulations with birthday ******

# ****** Start Manipulations with notes ******
@input_error
def add_note(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-note <name> <content>")

    name = args[0]
    content = " ".join(args[1:])

    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    note = record.add_note(content)
    return f"{Fore.GREEN}Note added successfully! ID: {note.id}"

@input_error
def show_notes(args, book: AddressBook):
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-notes <name>")

    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    notes = record.show_all_notes()
    if not notes:
        return f"{Fore.YELLOW}No notes for {name}"

    result = [f"{Fore.WHITE}Notes for {name}:"]
    for idx, note in enumerate(notes, 1):
        result.append(f"{Fore.CYAN}[{idx}] {note}")

    return "\n".join(result)

@input_error
def find_notes(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: find-notes <name> <search_text>")

    name = args[0]
    search_text = " ".join(args[1:])

    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    notes = record.find_notes(search_text)
    if not notes:
        return f"{Fore.YELLOW}No notes found for '{search_text}'"

    result = [f"{Fore.WHITE}Found {len(notes)} note(s) for '{search_text}':"]
    for idx, note in enumerate(notes, 1):
        result.append(f"{Fore.CYAN}[{idx}] {note}")

    return "\n".join(result)

@input_error
def edit_note(args, book: AddressBook):
    if len(args) < 3:
        raise InsufficientArgumentsError("Usage: edit-note <name> <note_id> <new_content>")

    name = args[0]
    note_id = args[1]
    new_content = " ".join(args[2:])

    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    if not record.edit_note(note_id, new_content):
        raise NoteNotFoundError(f"Note with ID '{note_id}' not found")
    
    return f"{Fore.GREEN}Note {note_id} updated successfully"

@input_error
def delete_note(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: delete-note <name> <note_id>")

    name = args[0]
    note_id = args[1]

    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")

    if not record.delete_note(note_id):
        raise NoteNotFoundError(f"Note with ID '{note_id}' not found")
    
    return f"{Fore.GREEN}Note {note_id} deleted successfully"

@input_error
def add_tag(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: add-tag <note_id> <tag>")
    
    note_id = args[0]
    tag = args[1]
    
    record, note = book.find_note_by_id(note_id)
    if not note:
        raise NoteNotFoundError(f"Note with ID '{note_id}' not found")
    
    note.add_tag(tag)
    return f"{Fore.GREEN}Tag '{tag}' added to note {note_id}"

@input_error
def remove_tag(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: remove-tag <note_id> <tag>")
    
    note_id = args[0]
    tag = args[1]
    
    record, note = book.find_note_by_id(note_id)
    if not note:
        raise NoteNotFoundError(f"Note with ID '{note_id}' not found")
    
    if not note.remove_tag(tag):
        raise ValueError(f"Tag '{tag}' not found in note {note_id}")
    
    return f"{Fore.GREEN}Tag '{tag}' removed from note {note_id}"

@input_error
def find_by_tag(args, book: AddressBook):
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: find-by-tag <name> <tag>")
    
    name = args[0]
    tag = args[1]
    
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    notes = record.find_notes_by_tag(tag)
    if not notes:
        return f"{Fore.YELLOW}No notes found with tag '{tag}'"
    
    result = [f"{Fore.WHITE}Notes for {name} with tag '#{tag}':"]
    for idx, note in enumerate(notes, 1):
        result.append(f"{Fore.BLUE}[{idx}] {note}")
    
    return "\n".join(result)

@input_error
def find_all_by_tag(args, book: AddressBook):
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: find-all-by-tag <tag>")
    
    tag = args[0]
    results = book.find_all_notes_by_tag(tag)
    
    if not results:
        return f"{Fore.YELLOW}No notes found with tag '{tag}'"
    
    output = [f"{Fore.WHITE}All notes with tag '#{tag}':"]
    for result in results:
        output.append(f"{Fore.WHITE}Contact: {result['contact']}")
        for idx, note in enumerate(result['notes'], 1):
            output.append(f"{Fore.BLUE}[{idx}] {note}")
    
    return "\n".join(output)

@input_error
def show_notes_sorted(args, book: AddressBook):
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: show-notes-sorted <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    notes = record.show_all_notes()
    if not notes:
        return f"{Fore.YELLOW}No notes for {name}"
    
    sorted_notes = sorted(notes, key=lambda n: len(n.tags), reverse=True)
    
    result = [f"{Fore.WHITE}Notes for {name} (sorted by tags count):"]
    for idx, note in enumerate(sorted_notes, 1):
        result.append(f"{Fore.CYAN}[{idx}] {note}")
    
    return "\n".join(result)

# ****** End Manipulations with notes ******

# ****** Start Manipulations with emails ******
@input_error
def add_email(args, book:AddressBook):
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
    if len(args) < 2:
        raise InsufficientArgumentsError("Usage: change-email <name> <email>")
    
    name, new_email = args
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.edit_email(new_email)
    return f"{Fore.GREEN}Email is updated"

@input_error    
def show_email(args, book:AddressBook):
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
    if len(args) < 1:
        raise InsufficientArgumentsError("Usage: delete-email <name>")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise ContactNotFoundError(f"Contact '{name}' not found")
    
    record.delete_email()
    return f"{Fore.GREEN}Email is removed"
# ****** End Manipulations with emails ******

def help():
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

def main():
    book = load_data()
    print(f"{Fore.LIGHTBLUE_EX}Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Fore.LIGHTBLUE_EX}Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "add-note":
            print(add_note(args, book))
        elif command == "add-tag":
            print(add_tag(args, book))
        elif command == "change-phone":
            print(update_contact(args, book))
        elif command == "change-birthday":
            print(update_birthday(args, book))
        elif command == "change-address":
            print(update_address(args, book))
        elif command == "change-email":
            print(update_email(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "delete-phone":
            print(delete_phone(args, book))
        elif command == "delete-birthday":
            print(delete_birthday(args, book))
        elif command == "delete-address":
            print(delete_address(args, book))
        elif command == "delete-email":
            print(delete_email(args, book))
        elif command == "delete-note":
            print(delete_note(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "show-phone":
            print(get_contact(args, book))
        elif command == "show-birthday":
            print(get_birthday(args, book))
        elif command == "show-birthdays-in":
            print(birthdays_in_range(args, book))
        elif command == "show-celebration-day":
            print(birthdays(book))
        elif command == "show-address":
            print(get_address(args, book))
        elif command == "show-notes":
            print(show_notes(args, book))
        elif command == "show-notes-sorted":
            print(show_notes_sorted(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        elif command == "edit-note":
            print(edit_note(args, book))
        elif command == "remove-tag":
            print(remove_tag(args, book))
        elif command == "find":
            print(find(args, book))
        elif command == "find-by-tag":
            print(find_by_tag(args, book))
        elif command == "find-all-by-tag":
            print(find_all_by_tag(args, book))
        elif command == "find-notes":
            print(find_notes(args, book))
        elif command == "help":
            print(help())
        else:
            print(f"{Fore.RED}Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()