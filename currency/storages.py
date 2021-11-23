'''
Contains storages for currencies data
'''
from abc import ABC, abstractmethod
from currency.parsers import CentralBankXMLParser


class BaseCurrencyStorage(ABC):
    '''Implements base currency storage'''
    def __init__(self, source: str) -> None:
        self._source = source
        self._currencies = None
        self._date = None
        self.get_currencies_data()

    @abstractmethod
    def get_currencies_data(self) -> None:
        '''Initialize currencies dict with data'''

    @property
    def currencies(self):
        '''Return currencies dict'''
        return self._currencies

    @property
    def date(self):
        '''Get date related to currencies data'''
        return self._date


class CurrencyStorageECB(BaseCurrencyStorage):
    '''Implements currency storage for European Central Bank'''

    def get_currencies_data(self) -> None:
        parser = CentralBankXMLParser(self._source)
        currencies_data = parser.get_currencies_data()
        self._currencies = currencies_data.get('currencies', {})
        self._date = currencies_data.get('date')
