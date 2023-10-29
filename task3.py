from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone:
    def __init__(self, value):
        self._value = None  

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not (isinstance(new_value, str) and new_value.isdigit() and len(new_value) == 10):
            raise ValueError("Invalid phone number format. Please provide a 10-digit phone number.")
        self._value = new_value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        # Валідація формату дня народження (приклад: 01.01.2000)
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Please provide a date in the format DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        try:
            new_phone = Phone(phone_number)
            self.phones.append(new_phone)
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        if not self.remove_phone(old_phone):
            return False
        return self.add_phone(new_phone)

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def __str__(self):
        phone_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name, None)

    def birthdays_this_week(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                if today <= birthday_date < next_week:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

def get_birthdays_per_week(book):
    upcoming_birthdays = book.birthdays_this_week()
    if upcoming_birthdays:
        print("Upcoming birthdays this week:")
        for record in upcoming_birthdays:
            print(record)
    else:
        print("No upcoming birthdays this week.")

class Bot:
    def __init__(self):
        self.book = AddressBook()

    def add_contact(self, name, phone):
        record = Record(name)
        if record.add_phone(phone):
            self.book.add_record(record)
            print(f"Contact {name} added with phone number {phone}.")
        else:
            print(f"Failed to add contact {name}.")
    
    def change_phone(self, name, new_phone):
        record = self.book.find(name)
        if record:
            if record.edit_phone(record.phones[0].value, new_phone):
                print(f"Phone number updated for contact {name}.")
            else:
                print(f"Failed to update phone number for contact {name}.")
        else:
            print(f"Contact {name} not found.")

    def show_phone(self, name):
        record = self.book.find(name)
        if record and record.phones:
            print(f"{name}'s phone number is {record.phones[0].value}.")
        elif record:
            print(f"{name} doesn't have a phone number set.")
        else:
            print(f"Contact {name} not found.")

    def show_all_contacts(self):
        if self.book:
            print("All contacts in the address book:")
            for record in self.book.data.values():
                print(record)
        else:
            print("Address book is empty.")

    def add_birthday(self, name, birthday):
        record = self.book.find(name)
        if record:
            if record.add_birthday(birthday):
                print(f"Birthday added for {name}.")
            else:
                print(f"Failed to add birthday for {name}.")
        else:
            print(f"Contact {name} not found.")

    def show_birthday(self, name):
        record = self.book.find(name)
        if record and record.birthday:
            print(f"{name}'s birthday is on {record.birthday.value}.")
        elif record:
            print(f"{name} doesn't have a birthday set.")
        else:
            print(f"Contact {name} not found.")

    def show_birthdays_this_week(self):
        get_birthdays_per_week(self.book)

    
    def greet(self):
        print("Hello! How can I assist you today?")

    def close_program(self):
        print("Closing the program.")
        exit()

    def process_command(self, command_line):
        command_parts = command_line.split()
        command = command_parts[0].lower().replace('-', '')  # Accept commands with or without dashes
        params = command_parts[1:]

        if command == "add":
            if len(params) == 2:
                self.add_contact(params[0], params[1])
            else:
                print("Invalid command. Usage: add [name] [phone]")
        elif command == "change":
            if len(params) == 2:
                self.change_phone(params[0], params[1])
            else:
                print("Invalid command. Usage: change [name] [new_phone]")
        elif command == "phone":
            if len(params) == 1:
                self.show_phone(params[0])
            else:
                print("Invalid command. Usage: phone [name]")
        elif command == "all":
            self.show_all_contacts()
        elif command == "addbirthday":
            if len(params) == 2:
                self.add_birthday(params[0], params[1])
            else:
                print("Invalid command. Usage: addbirthday [name] [DD.MM.YYYY]")
        elif command == "showbirthday":
            if len(params) == 1:
                self.show_birthday(params[0])
            else:
                print("Invalid command. Usage: showbirthday [name]")
        elif command == "birthdays":
            self.show_birthdays_this_week()
        elif command == "hello":
            self.greet()
        elif command == "close" or command == "exit":
            self.close_program()
        else:
            print("Invalid command. Type 'help' for a list of commands.")




if __name__ == "__main__":
    my_bot = Bot()

    while True:
        user_input = input("Enter a command: ")
        my_bot.process_command(user_input)
