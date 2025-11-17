from colorama import Fore, init
from data_storage import save_data, load_data
from command_suggester import CommandSuggester
from commands.registry import execute_command

init(autoreset=True)


def parse_input(user_input):
    """Parse user input into command and arguments."""
    commands = user_input.split()
    if not commands:
        return "", []
    cmd, *args = commands
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    """Main function to run the assistant bot."""
    book = load_data()
    suggester = CommandSuggester()
    
    print(f"{Fore.BLUE}Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ").strip()
        
        if not user_input:
            continue
        
        command, *args = parse_input(user_input)
        
        # Try to execute the command
        result = execute_command(command, args, book)
        
        if result == "EXIT":
            print(f"{Fore.BLUE}Good bye!")
            save_data(book)
            break
        elif result is not None:
            # Command executed successfully
            print(result)
        else:
            # Command not recognized, so try to suggest the closest command
            suggestion = suggester.suggest_command(command)
            
            if suggestion:
                print(f"{Fore.YELLOW}Command '{command}' not found. Maybe you meant '{Fore.CYAN}{suggestion}{Fore.YELLOW}'?")
            # If no suggestion is found, print an error message
            else:
                print(f"{Fore.RED}Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
