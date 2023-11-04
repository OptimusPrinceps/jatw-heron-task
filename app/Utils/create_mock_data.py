import base64
import hashlib
import time
from datetime import datetime, timedelta
from random import sample, randint

from Skeleton.transaction import Transaction


def generate_id(inputs=None, length=None, lowercase=False):
    remove_characters = ['+', '=', '-', '_']
    hash_string = str(time.time())
    if inputs is not None:
        hash_string += str(inputs)

    hash_bytes = hashlib.sha3_256(hash_string.encode()).digest()
    unique_id = base64.urlsafe_b64encode(hash_bytes).decode()
    for rc in remove_characters:
        unique_id = unique_id.replace(rc, str(randint(0, 9)))

    if lowercase:
        unique_id = unique_id.lower()
    if length is not None:
        return unique_id[:length]
    else:
        return unique_id


class TransactionFactory:
    @classmethod
    def create_transaction(cls) -> Transaction:
        amount = sample(range(-10000, 10000), 1)[0]
        if amount < 0:
            expenditures_and_category = [('pizza', 'food'), ('rick owens', 'shopping'), ('kebab', 'food'),
                                         ('fuel', 'transport'), ('factorio', 'entertainment'), ('shakes', 'food'),
                                         ('gym', 'health')]
            description, categories_default = sample(expenditures_and_category, 1)[0]

        else:
            income_and_category = [('job 1', 'salary'), ('job 2', 'salary'), ('interest', 'interest'), ('gift', 'gift'),
                                   ('feudal tithe', 'tax')]
            description, categories_default = sample(income_and_category, 1)[0]

        account_id = sample([str(i) for i in range(5)], 1)[0]
        balance = sample(range(-100000, 100000), 1)[0]
        currency = 'USD'
        end_user_id = account_id
        reference_id = generate_id()
        timestamp = datetime.now() + timedelta(days=randint(-100, 100))
        transaction_code = '1'

        transaction = Transaction(
            amount=amount,
            description=description,
            account_id=account_id,
            balance=balance,
            categories_default=categories_default,
            currency=currency,
            end_user_id=end_user_id,
            reference_id=reference_id,
            timestamp=timestamp,
            transaction_code=transaction_code
        )

        return transaction


if __name__ == "__main__":
    import pandas as pd

    n = 100

    transactions = [TransactionFactory.create_transaction() for _ in range(n)]
    transaction_dicts = [t.to_dict() for t in transactions]
    df = pd.DataFrame.from_records(transaction_dicts)
    df.to_csv('../../data/mydata.csv', index=False)
    print(df)
