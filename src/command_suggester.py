from difflib import get_close_matches
from typing import Optional


class CommandSuggester:
    """
    Suggests commands based on user input using fuzzy matching.
    """
    
    def __init__(self):
        self.commands = [
            "add", "delete", "all", "hello", "help", "close", "exit",
            "add-birthday", "add-address", "add-email", "add-note", "add-tag",
            "change-phone", "change-birthday", "change-address", "change-email",
            "show-phone", "show-birthday", "show-address", "show-email", "show-notes", "show-notes-sorted",
            "show-birthdays-in", "show-celebration-day",
            "delete-phone", "delete-birthday", "delete-address", "delete-email", "delete-note",
            "find", "find-notes", "find-by-tag", "find-all-by-tag",
            "edit-note", "remove-tag", "birthdays"
        ]
    
    def suggest_command(self, user_input: str) -> Optional[str]:
        if not user_input or not user_input.strip():
            return None
        
        # get_close_matches returns a list of closest matches
        # n=1 - return only the best variant
        # cutoff=0.6 - minimum similarity (from 0 to 1)
        matches = get_close_matches(user_input.lower(), self.commands, n=1, cutoff=0.6)
        
        return matches[0] if matches else None
