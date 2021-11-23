'''
Contains managers for Transaction and Device db models
'''
import csv
from enum import Enum
from sqlalchemy.sql import func, asc, desc
from transactions.models import Transaction, Device


class TransactionManager:
    '''Implements management class for Transaction model'''
    def __init__(self, session) -> None:
        self._session = session

    @property
    def session(self):
        '''Returns current db session'''
        return self._session

    def print_most_revenue_visitor(self) -> None:
        '''Prints out most revenue visitor'''
        session = self.session
        result = session.query(
           Transaction.visitor_id,
           func.sum(Transaction.revenue).label('total_revenue'),
        ).group_by(Transaction.visitor_id).order_by(
            desc('total_revenue')).first()

        print(
            f'visitor {result.visitor_id} created '
            f'the most revenue: {result.total_revenue}')

    def print_most_day_revenue(self, device_type=None) -> None:
        '''Prints out most day revenue for choosen device type'''
        query = self.session.query(
            Transaction.datetime,
            func.sum(Transaction.revenue).label('total_revenue')
        ).group_by(Transaction.datetime)
        if device_type is not None:
            query = query.filter(
                Transaction.device_type == device_type.value)
        result = query.order_by(desc('total_revenue')).first()
        print(
            f'A day which most revenue for '
            f'users who ordered via mobile '
            f'phone was {result.datetime.date()}: '
            f'total revenue is {result.total_revenue}')

    def convert_currency_to_euro(
            self, exchange_rate: float) -> None:
        '''Apply exchange rate for revenue and tax columns'''
        session = self.session
        print('First 5 rows before update')
        for transaction in session.query(
            Transaction
        ).order_by('id').all()[:5]:
            print(
                f'ID: {transaction.id}, '
                f'REVENUE: {transaction.revenue}, '
                f'TAX: {transaction.tax}')
        session.query(Transaction).update({
            Transaction.revenue: Transaction.revenue / exchange_rate
        })
        session.commit()
        print('First 5 rows after update')
        for transaction in session.query(
            Transaction
        ).order_by(asc('id')).all()[:5]:
            print(
                f'ID: {transaction.id}, '
                f'REVENUE: {transaction.revenue}, '
                f'TAX: {transaction.tax}')

    def dump_to_csv(self, filename: str) -> None:
        '''dump transactions and related devices data to csv'''
        total_data = self.session.query(
            Transaction, Device
        ).join(Device, Device.id == Transaction.device_type)
        transaction_columns = None
        device_columns = None
        header = None
        with open(filename, 'w') as out_csv:
            writer = csv.writer(out_csv, delimiter=',', quotechar='"')
            for transaction, device in total_data:
                if transaction_columns is None:
                    transaction_columns = transaction.__table__.columns.keys()
                if device_columns is None:
                    device_columns = [
                        column for column in device.__table__.columns.keys()
                        if column != 'id'
                    ]
                if header is None:
                    header = [*transaction_columns, *device_columns]
                    writer.writerow(header)
                writer.writerow([
                    *[getattr(
                            transaction, column_name
                        ) for column_name in transaction_columns],
                    *[getattr(
                            device, column_name
                        ) for column_name in device_columns]
                ])


class DeviceManager:
    '''Implements management class for Device model'''
    def __init__(self, session) -> None:
        self._session = session

    @property
    def session(self):
        '''Returns current db session'''
        return self._session

    def get_devices_as_enum(self) -> Enum:
        '''Returns devices as Enum object'''
        devices = self.session.query(Device).all()
        return Enum(
            'Devices',
            {device.device_name: device.id for device in devices}
        )
