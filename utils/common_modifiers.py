import pandas as pd
from typing import Callable, Any
import numpy as np
import math
from typing import Callable, Any
from .helpers import *


def categorize(feature: str, categories: dict):
    def inner(row):
        value = row[feature]
        if value is None or value is np.nan:
            return np.nan

        keys = categories.keys()
        if type(value) is list:
            result = []
            for v in value:
                if is_nan(v) or v not in keys:
                    result.append(np.nan)
                else:
                    result.append(categories[v])

            return result
        else:
            return categories[value]

    return inner


def extract_and_rename(cols: dict) -> callable:
    def inner_extractor(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        # print(cols, df.columns, cols.keys())

        df = df[cols.keys()]

        df.rename(columns=cols, inplace=True, )
        return df

    return inner_extractor


def rename(cols: dict) -> callable:
    def inner_extractor(src: pd.DataFrame) -> pd.DataFrame:
        src.rename(columns=cols, inplace=True)
        return src

    return inner_extractor


def add_const_driver(name: str, value) -> callable:
    def inner_modifier(src: pd.DataFrame) -> pd.DataFrame:
        src[name] = value
        return src

    return inner_modifier


def add_const_driver_many(drivers: dict) -> callable:
    def inner_modifier(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        for name, value in drivers.items():
            df[name] = value

        return df

    return inner_modifier


def combine_drivers(result: str, func: Callable[[pd.Series], Any]) -> callable:
    def inner_modifier(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        df[result] = df.apply(func, axis=1)
        return df

    return inner_modifier


def multi_unify_presence(drivers: [str]) -> Callable:
    def inner_unify_presence(row: pd.Series) -> int:
        for driver in drivers:
            if row[driver] == 1:
                return 1
        return 0

    return inner_unify_presence


def unify_presence(driver1: str, driver2: str) -> Callable:
    def inner_unify_presence(row: pd.Series) -> int:
        x = row[driver1]
        y = row[driver2]
        if x == 1 or y == 1:
            return 1
        else:
            return 0

    return inner_unify_presence


def sum_presence(driver1: str, driver2: str) -> Callable:
    def inner_sum_presence(row: pd.Series) -> int:
        x = row[driver1]
        y = row[driver2]
        return x + y

    return inner_sum_presence


def remove_drivers(drivers: [str]) -> callable:
    def inner_modifier(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        return df.drop(columns=drivers)

    return inner_modifier


def find_any(question, answer, found, not_found):
    """
    Parameters:
        question(str):  the question to be checked
        answer(Any): the answer to be checked
        found(str): the result if the answer is found
        not_found(str): the result if the answer is not found

    Returns:
        inner: the result of the check
    """

    def inner(row: pd.Series):
        if any(t == answer for t in row[question]):
            result = found
        else:
            result = not_found
        return result

    return inner


def transform(col: str, fn: Callable[[Any], Any]):
    def inner_transformer(df: pd.DataFrame) -> pd.DataFrame:
        df[col] = df[col].apply(fn)
        return df

    return inner_transformer


def transform_list(col: str, fn: Callable[[Any], Any]):
    def inner_transformer(df: pd.DataFrame) -> pd.DataFrame:
        df[col] = df[col].apply(fn)
        return df

    return inner_transformer


def int_each(x):
    result = []
    for i in x:
        if not is_nan(i):
            result.append(int(i))
        else:
            result.append(np.nan)
    return result


def transform_list_int(col: str):
    return transform_list(col, int_each)


def take(col: str, idx: int):
    def inner_transformer(df: pd.DataFrame) -> pd.DataFrame:
        df[col] = df[col].apply(lambda x: x[idx])
        return df

    return inner_transformer


def group(drivers: list):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, drivers)

        values = []
        for driver in drivers:
            values.append(row[driver])

        return values

    return inner


def take_one_with_value(drivers: list, search_value: Any, not_found_value: Any = np.nan):
    """
    Search with one driver with value {search_value} or return {not_found_value}
    :param drivers:  list of drivers (singular value) if the drivers is a list only take the first
    :param search_value: the value we are searching for
    :param not_found_value: the return value if none is found (default np.nan)
    :return:
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, drivers)
        values = []
        for driver in drivers:
            row_value = row[driver]
            if type(row_value) == list:
                values.append(row_value[0])
            else:
                values.append(row_value)

        for value in values:
            if value == search_value:
                return value

        return not_found_value

    return inner