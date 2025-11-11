from classes.address_book import AddressBook
from classes.record import Record

if __name__ == "__main__":
        # Створення книги
        book = AddressBook()

        # Додавання контактів
        john = Record("John")
        john.add_phone("1234567890")
        john.add_birthday("04.11.1988")
        book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("0987654321")
        jane.add_birthday("05.11.2000")
        book.add_record(jane)

        # Виведення
        for record in book.data.values():
            print(record)

        print("Дні народження наступного тижня:")
        for user in book.get_upcoming_birthdays():
            print(user)