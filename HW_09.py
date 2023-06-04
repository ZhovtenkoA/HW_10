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
        if command.startswith('add'):
             add_phones(command)
        elif command.startswith('change'):
             change_phones(command)
        elif command.startswith('phone'):
             print_phones(command)
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
def add_phones(command):
    global PHONES
    command_l = command.split()
    PHONES[command_l[1]] = command_l[2]
    

@input_error
def change_phones(command):
    global PHONES
    command_c = command.split()
    PHONES[command_c[1]] = command_c[2]
    

@input_error
def print_phones(command):
    command_g = command.split()
    result = PHONES.get(command_g[1], "Enter correct name")
    print(result)


def all_phones():
    return PHONES


PHONES = {}
COMMANDS = {
    'hello': say_hello(),
    'good bye': say_goodbye(),
    'close': say_goodbye(),
    'exit': say_goodbye(),
    'show all': all_phones()
}   

if __name__ == '__main__':
    main()
    