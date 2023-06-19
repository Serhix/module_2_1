from classes import Record, Name, Phone, Birthday, address_book
from abstract import AllBookRepresentation, OneRecordRepresentation, BirthdayRepresentation


def input_error(func):
    
    def wrapper(*args):        
        try:
            return func(*args)
        except KeyError:
            return "KeyError, maybe contact list is empty"
        except (IndexError, AttributeError, TypeError):
            return "Enter the correct command!!!"
        except ValueError as error:
            return str(error)
    return wrapper

def hello():
    return 'How can I help you?'

def add(data):                                    # додаємо новий номер до адресної книги(до існуючого або нового контакту)
    name, phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    record = address_book.get_record_from_book(name.value)
    if not record:
        record = Record(name.value)
    record.add_phone(phone.value)
    address_book.add_record(record)
    return 'Number added!'

def add_birthday(data):                                    # додаємо birthday(до існуючого або нового контакту)
    name, birthday = parse_data(data)
    name = Name(name)
    birthday = Birthday(birthday)
    record = address_book.get_record_from_book(name.value)
    if not record:
        record = Record(name.value)
    record.add_birthday(birthday.value)
    address_book.add_record(record)
    return 'Birthday added!'


def change(data):                     # міняємо номер phone на new_phone для контакту name
    name, phone, new_phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    new_phone = Phone(new_phone) 
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    record.change_phone(phone.value, new_phone.value)
    address_book.add_record(record)
    return f'The number {phone.value} has been changed to {new_phone.value} for contact {name.value}!'

def delete(data):                                # видаляємо номер phone для контакту name
    name, phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    record.delete_phone(phone.value)
    address_book.add_record(record)
    return f'The number {phone.value} has been delete for contact {name.value}!'

def info(data):                                 # пошук по name
    name = parse_data(data)[0]
    return OneRecordRepresentation(address_book, Name(name)).show()


def when_birthday(data):                        # пошук по name
    name = parse_data(data)[0]
    return BirthdayRepresentation(address_book, Name(name)).show()

def show_all(data):                             # показати всю книгу 
    N = int(parse_data(data)[0])
    return AllBookRepresentation(address_book, N).show()


def find(data):                                 #пошук співпадінь в name або phone
    matches = parse_data(data)[0]
    find_data = []
    all_phone = ''
    for record in address_book.data.values():
        for phone_number in record.phones:
            all_phone = ' '.join([all_phone, phone_number.value])
        if matches.lower() in record.name.value.lower() or matches in all_phone:
            find_data.append(str(record))
        all_phone = ''
    if find_data:
        return '\n'.join(find_data)
    else:
        return 'No matches found!'

def exit_func():
    return 'Good bye!'

def incorrect_input():
    return 'incorrect command input'

def parse_data(data):
    new_data = []
    for field in data.strip().split():
        new_data.append(field)
    return new_data


@input_error
def choise_comand(request):

    COMANDS = {
    'hello': hello,
    'show all' : show_all,
    'info': info,
    'add': add,
    'birthday': add_birthday,
    'change': change,
    'delete': delete,
    'close': exit_func, 
    'exit': exit_func,
    'good bye': exit_func,
    'when birthday': when_birthday,
    'find' : find

}
    comand = request
    data = ''
    for key in COMANDS:
        if request.strip().lower().startswith(key):
            comand = key
            data = request[len(comand):]
            break
    if data:
        return COMANDS.get(comand, incorrect_input)(data)
    return COMANDS.get(comand, incorrect_input)()