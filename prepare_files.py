'''Prepare files to run tech task'''
import requests


def main() -> None:
    '''main function'''
    db_url = 'https://transfer.feld-m.de/fbsharing/4cRHU5mL'
    currencies_url = 'https://transfer.feld-m.de/fbsharing/Bzu2Zj3y'
    with open('transactions.db', 'wb') as db_file:
        db_file.write(requests.get(db_url).content)
    with open('currencies.xml', 'wb') as currencies_file:
        currencies_file.write(requests.get(currencies_url).content)

if __name__ == '__main__':
    main()
