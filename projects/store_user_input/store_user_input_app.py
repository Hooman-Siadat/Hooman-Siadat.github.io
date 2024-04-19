from dataclasses import dataclass, asdict, astuple
from abc import ABC, abstractmethod
from os.path import getsize, exists
from json import dump, load
import csv
import logging
from datetime import date, datetime


@dataclass
class User:
    first_name: str
    last_name: str
    age: int


class DBManager(ABC):
    def __init__(self, file_path: str):
        self.file = file_path

    @abstractmethod
    def store(self, user: User):
        pass

    def is_empty(self):
        return getsize(self.file) == 0

    def is_created(self):
        return exists(self.file)


class TextManager(DBManager):
    def store(self, user: User):
        try:
            if not self.is_created() or self.is_empty():
                with open(self.file, 'w') as new_json_file:
                    dump([], new_json_file)
        except Exception as e:
            logging.error(f'{datetime.now()}\tSomething went wrong while creating the {
                          self.file}: {e}')
            return

        try:
            with open(self.file, 'r') as json_file:
                json_content = load(json_file)
        except Exception as e:
            logging.error(f'{datetime.now()}\tSomething went wrong while reading the {
                          self.file}: {e}')
            return

        json_content.append(asdict(user))

        try:
            with open(self.file, 'w') as json_file:
                dump(json_content, json_file, indent=4)
        except Exception as e:
            logging.error(f'{datetime.now()}\tSomething went wrong while writing the {
                          self.file}: {e}')
        else:
            logging.info(
                f'{datetime.now()}\tInformation successfully stored in {self.file}')


class CSVManager(DBManager):
    def store(self, user: User):
        try:
            if not self.is_created() or self.is_empty():
                with open(self.file, 'w', newline='') as new_csv_file:
                    header = ['FIRST NAME', 'LAST NAME', 'AGE']
                    csv_writer = csv.writer(new_csv_file)
                    csv_writer.writerow(header)
        except Exception as e:
            logging.error(f'{datetime.now()}\tSomething went wrong while creating the {
                          self.file}: {e}')
            return

        try:
            with open(self.file, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(astuple(user))
        except Exception as e:
            logging.error(f'{datetime.now()}\tSomething went wrong while writing the {
                          self.file}: {e}')
        else:
            logging.info(
                f'{datetime.now()}\tInformation successfully stored in {self.file}')


def main():
    text_file = 'users.json'
    csv_file = 'users.csv'
    repeat = True

    while repeat:
        ask = True
        try:
            fn = input('Please enter your first name:\t')
            ln = input('Please enter your last name:\t')
            age = int(input('Please enter your age:\t'))
        except ValueError as e:
            logging.error(f'{datetime.now()}\tInvalid user input: {e}')
        else:
            new_user = User(fn, ln, age)

            text_manager = TextManager(text_file)
            text_manager.store(new_user)

            csv_manager = CSVManager(csv_file)
            csv_manager.store(new_user)
        finally:
            while ask:
                try:
                    answer = input(
                        'Would you like to try again? (Y/N)\t').lower()
                except Exception as e:
                    logging.error('Invalid user input!')
                else:
                    if answer in ['y', 'n']:
                        if answer == 'n':
                            ask = False
                            repeat = False
                        else:
                            ask = False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='errors.log')
    main()
