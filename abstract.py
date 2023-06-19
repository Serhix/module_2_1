from abc import ABC, abstractmethod

class AbstractRepresentation(ABC):
    def __init__(self, data:dict, param: str) -> None:
        self.data = data
        self.param = param

    @abstractmethod
    def show(self):
        pass

class AllBookRepresentation(AbstractRepresentation):
    def show(self):
        all_book = ''
        page_number = 1
        for page in self.data.iterator(self.param):
            all_book += f'Page -- {page_number} -- \n'
            for record in page:
                all_book += f'{str(record)} \n'
            page_number += 1
        return all_book

class OneRecordRepresentation(AbstractRepresentation):   
    def show(self):
        record = self.data.get_record_from_book(self.param.value)
        if not record:
            return f'Contact with name {self.param.value} not found'
        return str(record)

class BirthdayRepresentation(AbstractRepresentation):
    def show(self):
        record = self.data.get_record_from_book(self.param.value)
        if not record:
            return f'Contact with name {self.param.value} not found'
        return record.days_to_birthday()