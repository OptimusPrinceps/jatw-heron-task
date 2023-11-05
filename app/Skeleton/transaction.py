"""
This file contains the Transaction class. Yes I am aware Heron has a Python client library.
"""
from datetime import datetime

import pandas as pd
import pytest


class TransactionConstants:
    AMOUNT = 'amount'
    DESCRIPTION = 'description'
    ACCOUNT_ID = 'account_id'
    BALANCE = 'balance'
    CATEGORIES_DEFAULT = 'categories_default'
    CURRENCY = 'currency'
    DATE = 'date'
    END_USER_ID = 'end_user_id'
    MCC_CODE = 'mcc_code'
    ORDER = 'order'
    REFERENCE_ID = 'reference_id'
    TIMESTAMP = 'timestamp'
    TRANSACTION_CODE = 'transaction_code'


class Transaction:
    """
    Heron transaction as per https://docs.herondata.io/api#tag/Transactions/paths/~1api~1transactions/post
    """

    def __init__(
            self,
            amount: float,
            description: str,
            account_id: str = None,
            balance: float = None,
            categories_default: str = None,
            currency: str = None,
            date: str or datetime = None,
            end_user_id: str = None,
            mcc_code: str = None,
            order: int = None,
            reference_id: str = None,
            timestamp: str or datetime = None,
            transaction_code: str = None
    ):
        self.amount = amount
        self.description = description
        self.account_id = account_id
        self.balance = balance
        self.categories_default = categories_default
        self.currency = currency

        if isinstance(date, str):
            date = pd.to_datetime(date)
        self.date: datetime = date

        self.end_user_id = end_user_id
        self.mcc_code = mcc_code
        self.order = order
        self.reference_id = reference_id

        if isinstance(timestamp, str):
            timestamp = pd.to_datetime(timestamp)
        self.timestamp: datetime = timestamp

        self.transaction_code = transaction_code

    def __str__(self):
        return f'Transaction(amount={self.amount}, description={self.description})'

    def __repr__(self):
        return str(self.to_dict())

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def to_dict(self) -> dict:
        return {
            TransactionConstants.AMOUNT: self.amount,
            TransactionConstants.DESCRIPTION: self.description,
            TransactionConstants.ACCOUNT_ID: self.account_id,
            TransactionConstants.BALANCE: self.balance,
            TransactionConstants.CATEGORIES_DEFAULT: self.categories_default,
            TransactionConstants.CURRENCY: self.currency,
            TransactionConstants.DATE: str(self.date),
            TransactionConstants.END_USER_ID: self.end_user_id,
            TransactionConstants.MCC_CODE: self.mcc_code,
            TransactionConstants.ORDER: self.order,
            TransactionConstants.REFERENCE_ID: self.reference_id,
            TransactionConstants.TIMESTAMP: str(self.timestamp),
            TransactionConstants.TRANSACTION_CODE: self.transaction_code
        }

    @classmethod
    def from_dict(cls, transaction_dict: dict) -> 'Transaction':
        return cls(**transaction_dict)


##############
# Unit tests #
##############

@pytest.fixture()
def transaction():
    return Transaction(
        amount=1.0,
        description='test',
        account_id='test',
        balance=1.0,
        categories_default='test',
        currency='test',
        date='2021-11-12T10:38:05Z',
        end_user_id='test',
        mcc_code='test',
        order=1,
        reference_id='test',
        timestamp='2021-11-12T10:38:05Z',
        transaction_code='test'
    )


def test_transaction_to_dict(transaction):
    expected_dict = {
        TransactionConstants.AMOUNT: 1.0,
        TransactionConstants.DESCRIPTION: 'test',
        TransactionConstants.ACCOUNT_ID: 'test',
        TransactionConstants.BALANCE: 1.0,
        TransactionConstants.CATEGORIES_DEFAULT: 'test',
        TransactionConstants.CURRENCY: 'test',
        TransactionConstants.DATE: '2021-11-12T10:38:05Z',
        TransactionConstants.END_USER_ID: 'test',
        TransactionConstants.MCC_CODE: 'test',
        TransactionConstants.ORDER: 1,
        TransactionConstants.REFERENCE_ID: 'test',
        TransactionConstants.TIMESTAMP: '2021-11-12T10:38:05Z',
        TransactionConstants.TRANSACTION_CODE: 'test'
    }

    # TODO: add assertion


def test_transaction_from_dict():
    transaction_dict = {
        "account_id": "checking_account_202348",
        "amount": -42.42,
        "balance": 423,
        "categories_default": "shopping",
        "currency": "USD",
        "date": "2020-04-27",
        "description": "GOOGLE *ADS12340929 cc@google.com US",
        "end_user_id": "my_best_customer_203948",
        "mcc_code": "string",
        "order": 0,
        "reference_id": "my_favourite_transaction_231098",
        "timestamp": "2021-11-12T10:38:05Z",
        "transaction_code": "card"
    }

    Transaction.from_dict(transaction_dict)

    # TODO: add assertion


def test_str_repr(transaction):
    transaction_str = str(transaction)
    assert transaction_str == 'Transaction(amount=1.0, description=test)'
