from collections import UserDict

class AddressBook(UserDict):    
    def add_record(self, record):
        self.data[record.name.value] = record
             
class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, phone):
        self.phone = phone


class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = Phone(phone)

    def show_phone(self):
        if self.phone:
            return self.phone.phone
        else:
            return "No phone number"

    def change_phone(self, phone):
        self.phone = Phone(phone)

    def delete_phone(self):
        self.phone = None


def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            print('Please, enter correct command')
            main()
        except IndexError:
            print('Give me name and phone please')
            main()
    return inner

def main():
    global PHONES
    running = True
    while running:
        command = input('Enter a command:  ').lower()
        command_list = command.split()
        if command_list[0] == 'add':
            try:
                name = command_list[1]
                phone = command_list[2]
                record = Record(name, phone)
                PHONES.add_record(record)
                print(f'add record for {name}')
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif command_list[0] == 'change':
            try:
                name = command_list[1]
                phone = command_list[2]
                record = PHONES.data.get(name)
                if record:
                    record.change_phone(phone)
                    print(f"Changed phone number for {name}")
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif command_list[0] =='phone':
            try:
                name = command_list[1]
                record = PHONES.data.get(name)
                if record:
                    phone = record.show_phone()
                    print(f"Phone number for {name}: {phone}")
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif command_list[0] == 'del':
            try:
                name = command_list[1]
                record = PHONES.data.get(name)
                if record:
                    record.delete_phone()
                    print(f"Deleted phone for {name}")
                else:
                    print(f"No record found for {name}")
            except (IndexError, TypeError, ValueError) as e:
                print(str(e))
        elif command_list[0] == 'show':
            try:
                if len(command_list) == 1:
                    for name, record in sorted(PHONES.items()):
                        phone = record.show_phone()
                        print(f"{name}: {phone}")
                elif len(command_list) == 2:
                    letter = command_list[1]
                    for name, record in sorted(PHONES.items()):
                        if name.startswith(letter):
                            phone = record.show_phone()
                            print(f"{name}: {phone}")
                else:
                    raise ValueError('Invalid command')
            except ValueError as e:
                print(str(e))
        else:
            print(get_handler(command))
            if get_handler(command) == 'Good bye!':
                running = False
        

@input_error
def get_handler(command):
    return COMMANDS[command]
        

def say_hello():
    output = 'How can I help you?'
    return output


def say_goodbye():
    output = 'Good bye!'
    return output

@input_error
def print_phones(command):
    command_g = command.split()
    result = PHONES.get(command_g[1], "Enter correct name")
    print(result)


def all_phones():
    all_records = ""
    for name, record in PHONES.items():
        phone = record.phone.phone
        all_records += f"{name}: {phone}\n"
    return all_records


PHONES = AddressBook()
COMMANDS = {
    'hello': say_hello(),
    'good bye': say_goodbye(),
    'close': say_goodbye(),
    'exit': say_goodbye(),
    'show all': all_phones()
}   

if __name__ == '__main__':
    main()
    