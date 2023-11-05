import random

import numpy as np
import pandas as pd

from Skeleton.constants import get_data_dir


def _preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by='date')
    df['date'] = pd.to_datetime(df['date'])
    return df


class _CandidateGroupingModel:
    @classmethod
    def group_by_description(cls, descriptions: pd.Series) -> list[[tuple[list, float]]]:
        """
        Normalises descriptions to find unique ones
        Returns a list of candidate groups along with a confidence associated with each grouping
        """

        normalised_descriptions = descriptions.copy()
        normalised_descriptions = normalised_descriptions.str.lower()
        unique_descriptions = normalised_descriptions.unique()
        named_entity_grouping = cls._identify_named_entity_grouping(unique_descriptions)
        levenstein_grouping = cls._identify_levenstein_grouping(unique_descriptions)
        substring_grouping = cls._identify_substring_ratio_grouping(unique_descriptions)

        return [*named_entity_grouping, *levenstein_grouping, *substring_grouping]

    @classmethod
    def _identify_named_entity_grouping(cls, descriptions: pd.Series) -> list[[tuple[list, float]]]:
        """
        Identifies named entities in descriptions
        """
        # TODO: implement this
        return [([d], 0.5) for d in descriptions]

    @classmethod
    def _identify_levenstein_grouping(cls, descriptions: pd.Series, max_distance=2) -> list[[tuple[list, float]]]:
        """
        Identifies similar descriptions using the Levenstein distance with an allowable maximum edit distance
        """
        # TODO: implement this
        return [([d], 0.6) for d in descriptions if random.random() > 0.2]

    @classmethod
    def _identify_substring_ratio_grouping(cls, descriptions: pd.Series, threshold=0.8) -> list[[tuple[list, float]]]:
        """
        Identifies similar descriptions using the substring ratio with an allowable threshold
        """
        # TODO: implement this
        return [([d], 0.7) for d in descriptions if random.random() > 0.3]


class _IntervalModel:
    @classmethod
    def compute_confidence(cls, dates: pd.Series) -> float:
        """
        Computes the intervals between the transactions in the group and ouptuts a confidence that the set of transactions is recurring
        """
        intervals = dates.diff()
        interval_stdev = intervals.std()
        # TODO: use a function to transform the standard deviation into a confidence
        return random.random()


class _AmountModel:
    @classmethod
    def compute_confidence(cls, amounts: pd.Series) -> float:
        """
        Computes the standard deviation of the amounts in the group and outputs a confidence that the set of transactions is recurring
        """
        amount_stdev = amounts.std()
        # TODO: use a function to transform the standard deviation into a confidence
        return random.random()


class _EnsembleModel:
    @classmethod
    def coalesce(cls, group_confidence: float, interval_confidence: float, amount_confidence: float) -> float:
        """
        Coalesces confidences from different models
        """
        # TODO: use an actual model with learnable weights to coalesce the confidences
        weighted_confidences = [group_confidence * 0.45, interval_confidence * 0.35, amount_confidence * 0.2]
        return np.mean(weighted_confidences)


def _identify_recurring_transactions(df: pd.DataFrame) -> list[tuple[list, float]]:
    """
    Identifies recurring transactions in a dataframe
    :param df: dataframe of transactions
    :return: a list where each entry is a tuple where the first entry is a list of the ids of a
    potentially identified set of recurring transactions and the second entry is a confidence that
    the set of transactions is recurring
    """
    df = _preprocess_df(df)

    candidate_groupings_with_confidence: list[tuple[list, float]] = (
        _CandidateGroupingModel.group_by_description(df['description']))

    recurring_transactions_with_probability = []
    for candidate_group, grouping_confidence in candidate_groupings_with_confidence:
        filtered_df = df[df['description'].str.lower().isin(candidate_group)]

        if len(filtered_df) == 1:
            # This is only necessary while bad candidates are generated (no recurring set will only have one transaction in it)
            continue

        interval_confidence = _IntervalModel.compute_confidence(filtered_df['date'])
        amount_confidence = _AmountModel.compute_confidence(filtered_df['amount'])

        recurring_confidence = _EnsembleModel.coalesce(grouping_confidence, interval_confidence, amount_confidence)
        recurring_transactions_with_probability.append((filtered_df.index.to_list(), recurring_confidence))

    # Sort by confidence in descending order
    recurring_transactions_with_probability.sort(key=lambda x: x[1], reverse=True)
    return recurring_transactions_with_probability


def identify_recurring_transactions(df: pd.DataFrame) -> list[tuple[list, float]]:
    recurring_transactions_with_probability = _identify_recurring_transactions(df)
    for recurring_transactions, probability in recurring_transactions_with_probability:
        print(f'Identified recurring transactions {recurring_transactions} with probability {probability}')

    return recurring_transactions_with_probability


def test_heron_data_task():
    df = pd.read_csv(get_data_dir() + '/upload.csv')
    df = identify_recurring_transactions(df)
    # TODO: write a reproduceable test here
    assert len(df) > 1
