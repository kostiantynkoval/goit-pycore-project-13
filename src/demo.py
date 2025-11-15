from unittest.mock import patch
from main import main, add_note as original_add_note
import time
from colorama import Fore, Style

note_ids = []

# Декоратор для збереження note_id
def capture_note_id_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if "Note added successfully! ID:" in result:
            note_id = result.split("ID:")[-1].strip()
            note_ids.append(note_id)
        return result
    return wrapper

# Декорована версія add_note
add_note_func = capture_note_id_decorator(original_add_note)

# Список команд
commands_template = [
    "hello",
    "add John 1234567890",
    "add-birthday John 01.12.1995",
    "add-address John 221B Baker Street, London",
    "add-email John john.watson@example.com",
    "add-note John Prepare medical report",
    "add-tag {last_note_id} medical",
    "find-by-tag John medical",
    "remove-tag {last_note_id} medical",
    "add-tag {last_note_id} detective",
    "find-all-by-tag detective",
    "show-phone John",
    "change-phone John 1234567890 9876543210",
    "show-phone John",
    "show-address John",
    "change-address John 221B Baker Street, London -> New London Address",
    "show-address John",
    "show-birthday John",
    "show-email John",
    "change-email John john.newmail@example.com",
    "show-email John",
    "show-birthdays-in 30",
    "change-birthday John 20.11.1995",
    "show-celebration-day",
    "add-note John Meet Sherlock at 8",
    "show-notes John",
    "show-notes-sorted John",
    "add John 3234567999",
    "all",
    "edit-note John {last_note_id} Meet Sherlock at 7",
    "find-notes John Sherlock",
    "delete-birthday John",
    "find name John",
    "delete-address John New London Address",
    "find name John",
    "delete-email John",
    "find name John",
    "delete-note John {last_note_id}",
    "find name John",
    "delete-phone John 9876543210",
    "find name John",
    "help",
    "close"
]

def mock_input(prompt):
    if commands_template:
        cmd = commands_template.pop(0)
        if "{last_note_id}" in cmd and note_ids:
            cmd = cmd.replace("{last_note_id}", note_ids[-1])
        print(f"{Fore.LIGHTWHITE_EX}{prompt}{cmd}{Style.RESET_ALL}")
        time.sleep(2)
        return cmd
    return "close"

# Перехоплюємо add_note через patch у main.py під час запуску main()
if __name__ == "__main__":
    with patch("main.add_note", add_note_func):
        with patch("builtins.input", side_effect=mock_input):
            main()
