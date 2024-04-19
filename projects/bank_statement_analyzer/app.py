import csv


class StatementCalculate:
    def __init__(self, csv_file, report_file):
        self.csv_file_path = csv_file
        self.result_file_path = report_file
        # csv file header
        self.header = ['Date', 'Description', 'Amount', 'Running Bal.']
        # lines to skip
        self.skip_lines = 8
        # line counter
        self.row_count = 0
        # amount spent
        self.spent = 0
        # amount earned
        self.earned = 0
        # report conent
        self.report = ''

    def analyze(self):
        try:
            # analyze csv file and calculate spent and earned
            with open(self.csv_file_path, 'r') as csv_file:
                reader_obj = csv.DictReader(csv_file, self.header)
                for record in reader_obj:
                    self.row_count += 1
                    if self.row_count > self.skip_lines:
                        amount = float(record['Amount'].replace(',', ''))
                        if amount > 0:
                            self.earned += amount
                        else:
                            self.spent += abs(amount)

        except FileNotFoundError as fnfe:
            print(f'File not found: {fnfe.filename}')
        except PermissionError as pe:
            print(f'Insufficient permission: {pe}')
        except OSError as ose:
            print(f'Something went wrong during read/write process: {ose}')
        except Exception as ee:
            print(f'Something went wrong: {ee}')
        else:
            self.report = [
                f'Earned a total of:\t{round(self.earned, ndigits=2)}',
                f'Spent a total of:\t{round(self.spent, ndigits=2)}',
                f'Difference:\t{
                    round(self.earned - self.spent, ndigits=2)}'
            ]
            # print report in terminal
            [print(line) for line in self.report]

    def generate_report(self):
        # write the report in the text file
        try:
            with open(self.result_file_path, 'w') as report_file:
                report_file.write('\n'.join(self.report))
                print('Report generated successfully!')
        except FileNotFoundError as fnfe:
            print(f'File not found: {fnfe.filename}')
        except PermissionError as pe:
            print(f'Insufficient permission: {pe}')
        except OSError as ose:
            print(f'Something went wrong during read/write process: {ose}')
        except Exception as ee:
            print(f'Something went wrong: {ee}')


def main():
    csv_file_path = input("Enter CSV file path: ")
    result_file_path = input("Enter result file path: ")

    statement = StatementCalculate(csv_file_path, result_file_path)
    statement.analyze()
    repeat = True

    while repeat:
        ask = input('Would you like to generate a report? (Y/N)\t').lower()
        if ask in 'yn':
            if ask == 'y':
                statement.generate_report()
                repeat = False
            else:
                repeat = False
        else:
            repeat = True


if __name__ == '__main__':
    main()
