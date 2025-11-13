from colorama import Fore, init
from data_storage import save_data, load_data
from classes.address_book import AddressBook
from classes.record import Record

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
        except ValueError as e:
            msg = str(e)
            if "unpack" in msg or "not enough values" in msg:
                return f"{Fore.RED}Give me name and phone please"
            return f"{Fore.RED}{msg}"
        except IndexError:
            return f"{Fore.RED}Enter user name"
        except KeyError:
            return f"{Fore.RED}Contact not found"

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = f"{Fore.GREEN} Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"{Fore.GREEN}Contact added"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return f"{Fore.RED}Usage: delete <name>"
    
    name = args[0]
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    confirmation=input(f"{Fore.YELLOW}Are you sure? You are going to delete the entire contact '{name}'? (yes/no):")
    if confirmation.strip().lower()!="yes":
        return f"{Fore.CYAN} Deletion cancelled."
    
    if book.delete(name):
        return f"{Fore.GREEN}Contact {name} deleted successfully"
    else:
        return f"{Fore.RED}Contact '{name}' not found"


@input_error
def update_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"{Fore.GREEN}Phone updated"
    else:
        raise KeyError

@input_error
def get_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones_str = "; ".join(p.value for p in record.phones) if record.phones else "N/A"
        lines = [
            f"{Fore.GREEN}Contact name: {record.name.value}",
            f"Phones: {phones_str}",
            "-----------------------"
        ]
        return "\n".join(lines)
    else:
        raise KeyError
    
@input_error
def delete_phone(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: delete-phone <name> <phone>"

    name = args[0]
    phone=args[1]
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    if len(record.phones) <=1:
        return f"{Fore.RED}Contact must have at least one phone number."
    
    if record.remove_phone(phone):
        return f"{Fore.GREEN}Phone number {phone} of contact {name} deleted successfully"
    else:
        return f"{Fore.RED}Phone number '{phone}' not found"

  

@input_error
def get_address(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        address_str = "; ".join(a.value for a in record.addresses) if record.addresses else "N/A"
        lines = [
            f"{Fore.CYAN}Contact name: {record.name.value}",
            f"Address: {address_str}",
            "-----------------------"
        ]
        return "\n".join(lines)
    else:
        raise KeyError
    

@input_error
def update_address(args, book: AddressBook):
    if len(args) < 3:
        return f"{Fore.RED}Usage: update-address <name> <old_address> -> <old_address>"
    
    name=args[0]
    rest=" ".join(args[1:])
    try:
        old_addr, new_addr = rest.split("->")
        old_addr = old_addr.strip()
        new_addr = new_addr.strip()
    except ValueError:
        return f"{Fore.RED}Please separate old and new addresses with '->'"
    record = book.find(name)

    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    if old_addr not in record.addresses:
        return f"{Fore.RED}Contact {name} has no address {old_addr}"
    
    if record.edit_address(old_addr, new_addr):
        return f"{Fore.GREEN}Address of the contact {name} updated"
    else:
        f"{Fore.RED}Contact {name} has no address {old_addr}"
    

@input_error
def delete_address(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: delete-address <name> <address>"
    
    name = args[0]
    address=" ".join(args[1:])
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    if record.remove_address(address):
        return f"{Fore.GREEN}Address {address} of contact {name} deleted successfully"
    else:
        return f"{Fore.RED}Address '{address}' not found"

@input_error
def get_all_contacts(book: AddressBook):
    if not book:
        return f"{Fore.YELLOW}Address book is empty"
    lines = []
    for record in book.data.values():
        phones_str = "; ".join(p.value for p in record.phones) if record.phones else "N/A"
        birthday_str = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A"
        address_str = "; ".join(a.value for a in record.addresses) if record.addresses else "N/A"
        lines.append(
            f"{Fore.GREEN}Contact name: {record.name.value}\n"
            f"Phones: {phones_str}\n"
            f"Birthday: {birthday_str}\n"
            f"Address: {address_str}\n"
            "-----------------------"
        )
    return "\n".join(lines)

@input_error
def add_birthday(args, book:AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{Fore.GREEN}Birthday added"
    else:
        raise KeyError

@input_error
def add_address(args, book:AddressBook):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record:
        record.add_address(address)
        return f"{Fore.GREEN}Address added"
    else:
        raise KeyError


@input_error
def get_birthday(args, book:AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        birthday_str = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A"
        lines = [
            f"{Fore.MAGENTA}Contact name: {record.name.value}",
            f"Birthday: {birthday_str}",
            "-----------------------"
        ]
        return "\n".join(lines)
    else:
       raise KeyError
    

@input_error
def delete_birthday(args, book: AddressBook):
    if len(args) < 1:
        return f"{Fore.RED}Usage: delete-birthday <name>"
    
    name = args[0]
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    if record.remove_birthday(name):
        return f"{Fore.GREEN}Birthday of contact {name} deleted successfully"
    else:
        return f"{Fore.RED}Contact '{name}' has no birthday date"


@input_error
def birthdays(book:AddressBook):
    if not book:
        raise KeyError
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
def add_note(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: add-note <name> <content>"
    
    name = args[0]
    content = " ".join(args[1:])
    
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    try:
        note = record.add_note(content)
        return f"{Fore.GREEN}Note added successfully! ID: {note.id}"
    except ValueError as e:
        return f"{Fore.RED}{str(e)}"

@input_error
def show_notes(args, book: AddressBook):
    if len(args) < 1:
        return f"{Fore.RED}Usage: show-notes <name>"
    
    name = args[0]
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    notes = record.show_all_notes()
    if not notes:
        return f"{Fore.YELLOW}No notes for {name}"
    
    result = [f"{Fore.CYAN}Notes for {name}:"]
    for idx, note in enumerate(notes, 1):
        result.append(f"{Fore.GREEN}[{idx}] {note}")
    
    return "\n".join(result)

@input_error
def find_notes(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: find-notes <name> <search_text>"
    
    name = args[0]
    search_text = " ".join(args[1:])
    
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    notes = record.find_notes(search_text)
    if not notes:
        return f"{Fore.YELLOW}No notes found for '{search_text}'"
    
    result = [f"{Fore.CYAN}Found {len(notes)} note(s) for '{search_text}':"]
    for idx, note in enumerate(notes, 1):
        result.append(f"{Fore.GREEN}[{idx}] {note}")
    
    return "\n".join(result)

@input_error
def edit_note(args, book: AddressBook):
    if len(args) < 3:
        return f"{Fore.RED}Usage: edit-note <name> <note_id> <new_content>"
    
    name = args[0]
    note_id = args[1]
    new_content = " ".join(args[2:])
    
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    try:
        if record.edit_note(note_id, new_content):
            return f"{Fore.GREEN}Note {note_id} updated successfully"
        else:
            return f"{Fore.RED}Note with ID '{note_id}' not found"
    except ValueError as e:
        return f"{Fore.RED}{str(e)}"

@input_error
def delete_note(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: delete-note <name> <note_id>"
    
    name = args[0]
    note_id = args[1]
    
    record = book.find(name)
    if not record:
        return f"{Fore.RED}Contact '{name}' not found"
    
    if record.delete_note(note_id):
        return f"{Fore.GREEN}Note {note_id} deleted successfully"
    else:
        return f"{Fore.RED}Note with ID '{note_id}' not found"
    
@input_error
def find(args, book: AddressBook):
    if len(args) < 2:
        return f"{Fore.RED}Usage: find <field> <string>"
    
    field = args[0]
    string = args[1]
    lines=[]
    records = book.find_by_any_arg(field, string)

    if len(records) == 0:
        return f"{Fore.RED}Contacts with the field {field} that contain {string} not found."
    else:
        for r in records:
            phones_str = "; ".join(p.value for p in r.phones) if r.phones else "N/A"
            birthday_str = r.birthday.value.strftime("%d.%m.%Y") if r.birthday else "N/A"
            address_str = "; ".join(a.value for a in r.addresses) if r.addresses else "N/A"
            lines.append(
            f"{Fore.GREEN}Contact name: {r.name.value}\n"
            f"Phones: {phones_str}\n"
            f"Birthday: {birthday_str}\n"
            f"Address: {address_str}\n"
            "-----------------------"
        )
    return "\n".join(lines)


def main():
    book = load_data()
    print(f"{Fore.BLUE}Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{Fore.BLUE}Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print(f"{Fore.BLUE}How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "change-phone":
            print(update_contact(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "show-phone":
            print(get_contact(args, book))
        elif command == "delete-phone":
            print(delete_phone(args, book))
        elif command == "show-birthday":
            print(get_birthday(args, book))
        elif command == "delete-birthday":
            print(delete_birthday(args, book))
        elif command == "show-address":
            print(get_address(args, book))
        elif command == "change-address":
            print(update_address(args, book))
        elif command == "delete-address":
            print(delete_address(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "add-note":
            print(add_note(args, book))
        elif command == "show-notes":
            print(show_notes(args, book))
        elif command == "find-notes":
            print(find_notes(args, book))
        elif command == "edit-note":
            print(edit_note(args, book))
        elif command == "delete-note":
            print(delete_note(args, book))
        elif command == "find":
            print(find(args, book))
        else:
            print(f"{Fore.RED}Invalid command")


if __name__ == "__main__":
    main()