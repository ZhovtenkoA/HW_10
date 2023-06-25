from collections import UserDict
from datetime import datetime, date
import re
import pickle
import os

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, name, phone=None, birthday=None):
        name = str(name)
        if name in self.data:
            raise ValueError(f"{name} already exists in the phone book")
        self.data[name] = Record(name, str(phone), birthday)
        PHONES[name] = self.data[name]

    def __iter__(self):
        return self.generator()

    def generator(self, n=1):
        count = 0
        for name, record in self.data.items():
            yield record
            count += 1
            if count == n:
                count = 0
                yield '*'*50
    
    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
    
    def load(self, file_name):
        try:
            search_file = os.stat(file_name + '.bin')
        except FileNotFoundError:
            print(f"File '{file_name}.bin' not found. Creating a new address book.")
            return

        with open(file_name + '.bin', 'rb') as f:
            data = pickle.load(f)
            self.data = data
    

    def search(self, pattern):
        for name, record in PHONES.data.items():
            if name.startswith(f'{pattern}'):
                print("_" * 50)
                print(f"{name}:")
                if record.phone is not None:
                    print(f"Phone: {record.phone.phone_number}")
                else:
                    print("No phone number")
                if record.birthday is not None:
                    print(f"Birthday: {record.birthday.birthday}")
                else:
                    print("No birthday")
                print()
            elif record.phone.phone_number.startswith(f'{pattern}'):
                print("_" * 50)
                print(f"{name}:")
                if record.phone is not None:
                    print(f"Phone: {record.phone.phone_number}")
                else:
                    print("No phone number")
                if record.birthday is not None:
                    print(f"Birthday: {record.birthday.birthday}")
                else:
                    print("No birthday")
                print()

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        pattern = r'^\+?\d{1,3}?\d{9,10}$'
        if not re.match(pattern, value):
            raise ValueError(f"Invalid phone number format: {value}")
        self.__phone_number = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        pattern = r'^\+?\d{1,3}?\d{9,10}$'
        if not re.match(pattern, value):
            raise ValueError(f"Invalid phone number format: {value}")
        self.__phone_number = value

    def __str__(self):
        return self.__phone_number


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        self._value = datetime.strptime(birthday, '%Y-%m-%d').date()

    @property
    def birthday(self):
        return self._value

    @birthday.setter
    def birthday(self, value):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValueError(f"Invalid birthday format: {value}")
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid birthday: {value}")
        self._value = datetime.strptime(value, '%Y-%m-%d').date()


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        if phone is not None:
            try:
                self.phone = Phone(phone)
            except ValueError as e:
                raise ValueError(f"Invalid phone number: {e}")
        else:
            self.phone = None
        if birthday is not None:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

    def __str__(self):
        return str(self.name).lower()

    def __repr__(self):
        return f"Record(name={self.name!r}, phone={self.phone!r}, birthday={self.birthday!r})"

    def show_phone(self):
        if self.phone:
            return self.phone.phone_number
        else:
           return "No phone number"

    def change_phone(self, phone):
        self.phone = Phone(phone)

    def delete_phone(self):
        self.phone = []

    def days_to_birthday(self):
        today = datetime.now().date()
        next_birthday = date(
            today.year, self.birthday.birthday.month, self.birthday.birthday.day)
        if next_birthday < today:
            next_birthday = date(
                today.year + 1, self.birthday.birthday.month, self.birthday.birthday.day)
        delta = next_birthday - today
        return delta.days



def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            print('Please enter a correct command')
            main()
        except IndexError:
            print('Please give me a name and phone number')
            main()
    return inner

def main():
    global PHONES
    running = True
    PHONES.load("auto_save")
    while running:
        #PHONES.load("auto_save")
        command = input('Enter a command:  ').lower()
        parts = command.split()
        action = parts[0]
        if action == "add":
            try:
                name = parts[1]
                phone = parts[2] if len(parts) > 2 else None
                birthday = parts[3] if len(parts) > 3 else None
                PHONES.add_record(name, phone, birthday)
                print(f"Added record for {name}")
                PHONES.save("auto_save")
                continue
            except ValueError as e:
                print(str(e))
        elif action == 'change':
            try:
                name = parts[1]
                phone = parts[2]
                record = PHONES.data.get(name)
                if record:
                    record.change_phone(phone)
                    print(f"Changed phone number for {name}")
                    PHONES.save("auto_save")
                    continue
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif action == 'phone':
            try:
                name = parts[1]
                record = PHONES.data.get(name)
                if record:
                    phone = record.show_phone()
                    if phone:
                        print(f"Phone: {phone}")
                        continue
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif action == 'del':
            try:
                name = parts[1]
                record = PHONES.data.get(name)
                if record:
                    record.delete_phone()
                    print(f"Deleted phone for {name}")
                    PHONES.save("auto_save")
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        
        elif action == 'show':
            display_all()
            continue
        elif action == 'iteration':
            for entry in PHONES.generator(n=2):
                if isinstance(entry, Record):
                    print("_" * 50)
                    print(f"Name: {entry.name},\nPhone: {entry.show_phone()},\nBirthday: {entry.birthday}\n")
                else:
                    print(entry)
        elif action == 'birthday':
            if len(parts) != 2:
                    print('Wrong number of arguments. Usage: birthday [name]')
                    return None
            name = parts[1]
            show_birthday(name)
            continue
        elif command == 'birthdays':
            show_birthdays()
            continue
        elif action == 'save':
            file_name = input("File name: ")
            return PHONES.save(file_name)
        elif action == 'load':
            file_name = input("File name: ")
            return PHONES.load(file_name)
        if command == 'search':
            pattern = input("Search pattern: ")
            results = PHONES.search(pattern)
        else:
            print(get_handler(command))
            if get_handler(command) == 'Good bye!':
                running = False

def get_handler(command):
    command = command.lower()
    if command == 'hello':
        return say_hello()
    elif command == 'good bye' or command == 'close' or command == 'exit':
        return say_goodbye()
    else:
        return 'Unknown command'
    
def say_hello():
    output = 'How can I help you?'
    return output
def say_goodbye():
    output = 'Good bye!'
    return output



def show_birthdays():
    for name, record in PHONES.data.items():
        if record.birthday is not None:
            birthday_str = record.birthday.birthday.strftime('%Y-%m-%d')
            print(f"{name}'s birthday is on {birthday_str}.")

def show_birthday(name):
    record = PHONES.get(name)
    if record is None:
        print(f"No record found for {name}.")
    elif not hasattr(record, 'birthday'):
        print(f"No birthday found for {name}.")
    else:
        days = record.days_to_birthday()
        if days == 0:
            print(f"Today is {name}'s birthday!")
        elif days == 1:
            print(f"{name}'s birthday is tomorrow!")
        else:
            print('Birthday:')
            print(f"{name}'s birthday is in {days} days.")


def display_all():
    for name, record in PHONES.data.items():
        print("_" * 50)
        print(f"{name}:")
        if record.phone is not None:
            print(f"Phone: {record.phone.phone_number}")
        else:
            print("No phone number")
        if record.birthday is not None:
            print(f"Birthday: {record.birthday.birthday}")
        else:
            print("No birthday")
        print()

PHONES = AddressBook()
COMMANDS = {
    'hello': say_hello,
    'good bye': say_goodbye,
    'close': say_goodbye,
    'exit': say_goodbye,
}

if __name__ == '__main__':
    main()
    