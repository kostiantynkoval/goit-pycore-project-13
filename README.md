# Personal Assistant Bot

A minimalistic command-line personal assistant for managing contacts, birthdays, addresses, emails, and notes with tags.

## Features

- **Contact Management**: Add, update, delete, and search contacts
- **Phone Numbers**: Multiple phone numbers per contact with full CRUD operations
- **Birthdays**: Track birthdays and get upcoming birthday reminders
- **Addresses**: Store and manage multiple addresses per contact
- **Emails**: Add and manage email addresses with validation
- **Notes System**: Add notes to contacts with full text search
- **Tag Support**: Organize notes with tags and search by tags
- **Data Persistence**: Automatic save/load using pickle
- **Command Suggestions**: Get suggestions for mistyped commands
- **Colorized Output**: Beautiful colored terminal interface

## Installation

### Setup Environment

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python src/main.py
```

## Available Commands

### Contact Operations

| Command  | Usage                   | Description                                      |
| -------- | ----------------------- | ------------------------------------------------ |
| `add`    | `add <name> <phone>`    | Add a new contact with a phone number            |
| `delete` | `delete <name>`         | Delete an entire contact (requires confirmation) |
| `all`    | `all`                   | Display all contacts in the address book         |
| `find`   | `find <field> <string>` | Search contacts by specific fields               |

### Phone Number Operations

| Command        | Usage                                         | Description                                |
| -------------- | --------------------------------------------- | ------------------------------------------ |
| `change-phone` | `change-phone <name> <old_phone> <new_phone>` | Update a phone number                      |
| `show-phone`   | `show-phone <name>`                           | Display all phone numbers for a contact    |
| `delete-phone` | `delete-phone <name> <phone>`                 | Remove a phone number (minimum 1 required) |

### Birthday Operations

| Command                | Usage                               | Description                                     |
| ---------------------- | ----------------------------------- | ----------------------------------------------- |
| `add-birthday`         | `add-birthday <name> <birthday>`    | Add birthday (format: DD.MM.YYYY)               |
| `show-birthday`        | `show-birthday <name>`              | Display birthday for a contact                  |
| `change-birthday`      | `change-birthday <name> <birthday>` | Update birthday date                            |
| `delete-birthday`      | `delete-birthday <name>`            | Remove birthday information                     |
| `show-celebration-day` | `show-celebration-day`              | Show contacts with birthdays in the next 7 days |
| `show-birthdays-in`    | `show-birthdays-in <days>`          | Show birthdays in the next N days               |

### Address Operations

| Command          | Usage                                                  | Description                          |
| ---------------- | ------------------------------------------------------ | ------------------------------------ |
| `add-address`    | `add-address <name> <address>`                         | Add an address to a contact          |
| `show-address`   | `show-address <name>`                                  | Display addresses for a contact      |
| `change-address` | `change-address <name> <old_address> -> <new_address>` | Update an address (use -> separator) |
| `delete-address` | `delete-address <name> <address>`                      | Remove an address                    |

### Email Operations

| Command        | Usage                         | Description                 |
| -------------- | ----------------------------- | --------------------------- |
| `add-email`    | `add-email <name> <email>`    | Add an email address        |
| `show-email`   | `show-email <name>`           | Display email for a contact |
| `change-email` | `change-email <name> <email>` | Update email address        |
| `delete-email` | `delete-email <name>`         | Remove email address        |

### Note Operations

| Command             | Usage                                      | Description                     |
| ------------------- | ------------------------------------------ | ------------------------------- |
| `add-note`          | `add-note <name> <content>`                | Add a note to a contact         |
| `show-notes`        | `show-notes <name>`                        | Display all notes for a contact |
| `show-notes-sorted` | `show-notes-sorted <name>`                 | Show notes sorted by tag count  |
| `find-notes`        | `find-notes <name> <search_text>`          | Search notes by text content    |
| `edit-note`         | `edit-note <name> <note_id> <new_content>` | Update note content             |
| `delete-note`       | `delete-note <name> <note_id>`             | Remove a note                   |

### Tag Operations

| Command           | Usage                        | Description                           |
| ----------------- | ---------------------------- | ------------------------------------- |
| `add-tag`         | `add-tag <note_id> <tag>`    | Add a tag to a note                   |
| `remove-tag`      | `remove-tag <note_id> <tag>` | Remove a tag from a note              |
| `find-by-tag`     | `find-by-tag <name> <tag>`   | Find notes of a contact by tag        |
| `find-all-by-tag` | `find-all-by-tag <tag>`      | Find notes across all contacts by tag |

### General Commands

| Command          | Description                    |
| ---------------- | ------------------------------ |
| `hello`          | Greet the bot                  |
| `help`           | Display all available commands |
| `close` / `exit` | Save and exit the application  |

## Usage Examples

```bash
# Add a contact
add John 1234567890

# Add birthday
add-birthday John 15.05.1990

# Add an address
add-address John 123 Main St, New York

# Add email
add-email John john@example.com

# Add a note
add-note John Remember to call back

# Add tag to a note (use the note ID from add-note output)
add-tag abc123 important

# Search for upcoming birthdays
show-birthdays-in 30

# Find contacts by phone
find phone 1234

# Change address (use -> separator)
change-address John 123 Main St -> 456 Oak Ave

# View all contacts
all
```

## Data Storage

The application automatically saves data to `addressbook.pkl` in the root directory. Data is loaded on startup and saved when you exit using the `close` or `exit` commands.

## Development

### Update Dependencies

If you add new libraries to the project:

```bash
pip freeze > requirements.txt
```

### Git Workflow

Check current branch:

```bash
git status
```

Create a new branch:

```bash
git checkout -b <branch_name>
```

## Project Structure

```
├── src/
│   ├── main.py              # Main application entry point
│   ├── commands/            # Command implementations (modular structure)
│   │   ├── __init__.py      # Package exports
│   │   ├── registry.py      # Command registry and entry point
│   │   ├── decorators.py    # Error handling decorator
│   │   ├── contact_commands.py   # Contact operations
│   │   ├── phone_commands.py     # Phone operations
│   │   ├── address_commands.py   # Address operations
│   │   ├── birthday_commands.py  # Birthday operations
│   │   ├── note_commands.py      # Note and tag operations
│   │   ├── email_commands.py     # Email operations
│   │   ├── general_commands.py   # Help, exit, etc.
│   ├── classes/             # Data model classes
│   │   ├── address_book.py  # AddressBook class
│   │   ├── record.py        # Contact record
│   │   ├── field.py         # Base field class
│   │   ├── name.py          # Name field
│   │   ├── phone.py         # Phone field
│   │   ├── address.py       # Address field
│   │   ├── birthday.py      # Birthday field
│   │   ├── email.py         # Email field
│   │   └── note.py          # Note class with tags
│   ├── exceptions/          # Custom exception classes
│   ├── command_suggester.py # Command suggestion logic
│   └── data_storage.py      # Persistence layer
├── addressbook.pkl          # Data storage file (auto-generated)
├── requirements.txt         # Python dependencies
└── README.md               # Readme
```
