import pandas as pd
from typing import Callable, Any


def extract_and_rename(cols: dict) -> callable:
    def inner_extractor(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        # print(cols, df.columns, cols.keys())

        df = df[cols.keys()]
        df.head()
        df.rename(columns=cols, inplace=True)
        return df

    return inner_extractor


def add_const_driver(name: str, value) -> callable:
    def inner_modifier(src: pd.DataFrame) -> pd.DataFrame:
        df = src.copy()
        df[name] = value
        return df

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
