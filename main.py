'''Main script'''
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from currency.storages import CurrencyStorageECB
from transactions.managers import DeviceManager, TransactionManager

def main() -> None:
    '''Main function'''
    config = configparser.ConfigParser()
    config.read('config.ini')

    connection_string = config.get('Settings', 'connection_string')
    currencies_path = config.get('Settings', 'currencies_path')

    engine = create_engine(connection_string)
    session_maker = sessionmaker(engine)
    with session_maker() as session:
        currencies_storage = CurrencyStorageECB(currencies_path)
        currencies = currencies_storage.currencies

        device_manager = DeviceManager(session)
        devices = device_manager.get_devices_as_enum()
        transaction_manager = TransactionManager(session)
        transaction_manager.print_most_revenue_visitor()
        transaction_manager.print_most_day_revenue(devices['Mobile Phone'])
        transaction_manager.convert_currency_to_euro(
            currencies.get('USD', 1)
        )
        transaction_manager.dump_to_csv('transactions.csv')

if __name__ == '__main__':
    main()
