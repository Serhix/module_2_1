from collections import UserDict
from datetime import datetime
import pickle


class AddressBook(UserDict):    # Наслідується від UserDict, словник з полями name, phone....
    def __init__(self):
        super().__init__()
        self.load_from_file()

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_record_from_book(self, name):
        for record in self.data.values():
            if record.name.value.lower() == name.lower():
                return record
        return None

    def iterator(self, N = 3):
        data_output = []
        iter_index = 0
        for record in self.data.values():
            data_output.append(record)
            iter_index += 1
            if iter_index >= N:
                yield data_output 
                data_output = []
                iter_index = 0
        if data_output:
            yield data_output
    
    def save_to_file(self):
        with open('address_book.dat', 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        try:   
            with open('address_book.dat', 'rb') as file:
                self.data = pickle.load(file)
        except:
            print('New contact book is created')

        
        
class Record:                   # Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.
  
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ''

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def delete_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                self.phones.remove(phone_number)
                break

    def change_phone(self, phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                phone_number.value = new_phone
                break
    
    def days_to_birthday(self):

        str_to_date = datetime(day = int(self.birthday.value.split('.')[0]), month = int(self.birthday.value.split('.')[1]), year = int(self.birthday.value.split('.')[2]))
        if self.birthday:
            birthday_in_this_year = datetime(
                year=datetime.now().year, 
                month=str_to_date.month, 
                day=str_to_date.day
            )
            if birthday_in_this_year.date() == datetime.now().date():
                return 'Birthday today'
            elif birthday_in_this_year.date() < datetime.now().date():
                how_many_days = datetime(year=datetime.now().year + 1, month=birthday_in_this_year.month, day=birthday_in_this_year.day) - datetime.now()
            else:
                how_many_days = datetime(year=datetime.now().year, month=birthday_in_this_year.month, day=birthday_in_this_year.day) - datetime.now()
            return f'Birthday in {how_many_days.days} days!'
        return f'No birthday added for contact {self.name.value}'
    
    def __str__(self) -> str:

        if self.birthday:
            return f'Name: {self.name.value}, phone: {", ".join(j.value for j in self.phones)}, birthday: {self.birthday.value}!'
        return f'Name: {self.name.value}, phone: {", ".join(j.value for j in self.phones)}'         


    
    

class Field:                    # Батьківський для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів.

    def __init__(self, value):
        self.__value = None
        self.value = value


class Name(Field):              # Обов'язкове поле з ім'ям

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if new_value and not new_value.isnumeric():
            self.__value = new_value

    

class Phone(Field):             # Необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if new_value.isnumeric():
            self.__value = new_value



class Birthday(Field):             # Необов'язкове поле з днем народження. може бути лише одне

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        # дату вводити в форматі дд.мм.рррр.
        birthday_date = datetime(day = int(new_value.split('.')[0]), month = int(new_value.split('.')[1]), year = int(new_value.split('.')[2]))
        # birthday_date = str_to_date(new_value)
        if birthday_date.year > 1900 and birthday_date <= datetime.now():
            self.__value = new_value

address_book = AddressBook()