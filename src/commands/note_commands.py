"""Commands for managing notes."""

from colorama import Fore
from classes.address_book import AddressBook
from exceptions import (
    ContactNotFoundError,
    NoteNotFoundError,
    InsufficientArgumentsError,
)
from commands.decorators import input_error


@input_error
def add_note(args, book: AddressBook):
    """Add a note to a contact."""
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
    """Show all notes for a contact."""
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
    """Find notes by search text."""
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
    """Edit a note."""
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
    """Delete a note."""
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
    """Add a tag to a note."""
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
    """Remove a tag from a note."""
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
    """Find notes by tag for a specific contact."""
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
    """Find notes by tag across all contacts."""
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
    """Show notes sorted by tags count."""
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

