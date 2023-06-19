from instructions_func import choise_comand
from classes import address_book

def main():

    try:
        while True:
            request = input('- ').lower()
            result = choise_comand(request)
            print(result)
            if result == 'Good bye!':
                break
    finally:    
        address_book.save_to_file()


if __name__ == '__main__':
    main()