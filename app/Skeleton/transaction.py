"""
This file contains the Transaction class. Yes I am aware Heron has a Python client library.
"""
from datetime import datetime

import pandas as pd
import pytest


class TransactionConstants:
    AMOUNT = 'amount'
    DESCRIPTION = 'description'
    DATE = 'date'


class Transaction:
    """
    Heron transaction as per https://docs.herondata.io/api#tag/Transactions/paths/~1api~1transactions/post
    """

    def __init__(
            self,
            amount: float,
            description: str,
            date: str or datetime = None,
    ):
        self.amount = amount
        self.description = description
        if isinstance(date, str):
            date = pd.to_datetime(date)
        self.date: datetime = date

    def __str__(self):
        return f'Transaction({self.amount} for {self.description} on {self.date})'

    def __repr__(self):
        return str(self.to_dict())

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def to_dict(self) -> dict:
        return {
            TransactionConstants.AMOUNT: self.amount,
            TransactionConstants.DESCRIPTION: self.description,
            TransactionConstants.DATE: str(self.date)
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
        date='2021-11-12'
    )


def test_transaction_to_dict(transaction):
    expected_dict = {
        TransactionConstants.AMOUNT: 1.0,
        TransactionConstants.DESCRIPTION: 'test',
        TransactionConstants.DATE: '2021-11-12'
    }

    # TODO: add assertion


def test_transaction_from_dict():
    transaction_dict = {
        "amount": -42.42,
        "date": "2020-04-27",
        "description": "GOOGLE *ADS12340929 cc@google.com US",
    }

    Transaction.from_dict(transaction_dict)

    # TODO: add assertion


def test_str_repr(transaction):
    transaction_str = str(transaction)
    assert transaction_str == 'Transaction(1.0 for test on 2021-11-12)'
