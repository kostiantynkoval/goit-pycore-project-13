from collections import UserDict
from datetime import datetime, timedelta
from .record import Record

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
         del self.data[name]
         return True
        return False

    def get_upcoming_birthdays(self):
        current_day = datetime.today().date()
        birthdays_list = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=current_day.year)

                # Check if the birthday has passed, if so, postpone it to next year
                if birthday_this_year < current_day:
                   birthday_this_year = birthday_this_year.replace(year=current_day.year + 1)

                days_till_birthday = (birthday_this_year - current_day).days

                # Check if birthday is in the next 7 days
                if 0 <= days_till_birthday <= 7:
                     celebration_date = birthday_this_year

                     # Check if celebration_date is on a weekend
                     if celebration_date.weekday() == 5:  # субота
                        celebration_date += timedelta(days=2)
                     elif celebration_date.weekday() == 6:  # неділя
                        celebration_date += timedelta(days=1)

                     birthdays_list.append({
                              "name": record.name.value,
                              "congratulation_date": celebration_date.strftime("%d.%m.%Y")
                     })

        return birthdays_list
    
    def find_all_notes_by_tag(self, tag: str):
        results = []
        for record in self.data.values():
            notes = record.find_notes_by_tag(tag)
            if notes:
                results.append({
                    'contact': record.name.value,
                    'notes': notes
                })
        return results
    
    def find_note_by_id(self, note_id: str):
        for record in self.data.values():
            note = record.find_note_by_id(note_id)
            if note:
                return record, note
        return None, None
        
    def find_by_any_arg(self, field: str, string: str) -> list[Record]:
        field=field.lower()
        string=string.lower()
        result: list[Record] = []
        for key, record in self.data.items():
            match field:
                case "name":
                    if string in key.lower():
                        result.append(record)
                case "phone":
                    if any(string in p.value for p in record.phones):
                        result.append(record)
                case "address":
                    if record.addresses and any(string in p.value.lower() for p in record.addresses):
                        result.append(record)
                case "birthday":
                    if record.birthday and string in record.birthday.value.strftime("%d.%m.%Y"):
                        result.append(record)
                case "email":
                    if record.email and string in record.email.value:
                        result.append(record)
                case _:
                    raise ValueError(f"Unknown field: {field}. Expected fields to search are: name, phone, birthday, address.")
        return result
