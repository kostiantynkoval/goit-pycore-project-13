"""Decorator for error handling in commands."""

from colorama import Fore
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
from classes.record import EmailFieldError


def input_error(func):
    """Decorator to handle common exceptions in command functions."""
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

