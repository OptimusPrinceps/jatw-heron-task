import pandas as pd


def heron_data_task(df: pd.DataFrame) -> pd.DataFrame:
    df.groupby('categories_default')['amount'].sum()
    return df

