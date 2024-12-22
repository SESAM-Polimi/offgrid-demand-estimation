import pandas as pd
from .helpers import *
import ast
import re


def transform_list(col):
    def inner(row: pd.Series):
        value = row[col]
        if is_nan(value):
            return np.nan
        nan_regex = r"nan,"
        last_nan_regex = r"nan]"
        value = re.sub(nan_regex, "", value)
        return re.sub(last_nan_regex, "]", value)

    return inner


"""
Check if the column is a list and take the first element
"""


def take_first(col: str):
    def inner(row: pd.Series):
        assert_column_exists_in_row(row, col)
        value = row[col]
        if is_nan(value):
            return np.nan
        if type(value) == str:
            if "[" not in value or "]" not in value:
                return value
        else:
            return value
        try:
            ast_value = ast.literal_eval(value)
        except Exception as e:
            print(f"Error in take_first: {e}", value)
            ast_value = value

        if type(ast_value) == list:
            if len(ast_value) > 0:
                return ast_value[0]
            else:
                return np.nan
        else:
            return ast_value

    return inner


def add_missing_flag(ref_col, missing_value):
    def inner(row: pd.Series):
        assert_column_exists_in_row(row, ref_col)
        value = row[ref_col]
        if value == missing_value:
            return 1
        return 0

    return inner


def replace_value(ref_col, old_value, new_value):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = df[ref_col].replace(old_value, new_value)
        return df

    return inner


def fillna(ref_col, new_value):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = df[ref_col].fillna(new_value)
        return df

    return inner

def fillna_with_mean(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = df[ref_col].fillna(df[ref_col].mean())
        return df

    return inner

def interpolate(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = df[ref_col].interpolate()
        return df
    return inner


def astype(ref_col, new_type):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = df[ref_col].astype(new_type)
        return df

    return inner


def categorize(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        value_counts = df[ref_col].value_counts()
        categories = {}
        for k, v in enumerate(value_counts.index):
            if is_nan(v):
                categories[v] = np.nan
            if v == -1:
                categories[v] = -1
            else:
                categories[v] = k + 1

        df[ref_col] = df[ref_col].replace(categories)
        return df

    return inner


def remove_row(ref_col, value):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df = df[df[ref_col] != value]
        return df

    return inner


def add_one_hot_encoding(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df = pd.concat([df, pd.get_dummies(df[ref_col], prefix=ref_col)], axis=1)
        df = df.drop(ref_col, axis=1)
        return df

    return inner


def min_max_normalize(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        df[ref_col] = (df[ref_col] - df[ref_col].min()) / (df[ref_col].max() - df[ref_col].min())
        return df

    return inner


def standardize(ref_col):
    def inner(src: pd.DataFrame):
        df = src.copy()
        series = df[ref_col]
        # Step 1: Normalize to [0, 1]
        min_val = series.min()
        max_val = series.max()
        normalized_series = (series - min_val) / (max_val - min_val)

        # Step 2: Scale to [-0.5, 0.5]
        scaled_series = normalized_series - 0.5
        df[ref_col] = scaled_series
        return df

    return inner


def merge_categories(ref_col, category_map):
    def inner(row: pd.Series):
        assert_column_exists_in_row(row, ref_col)

        value = row[ref_col]

        mapped_value = category_map[value]
        return mapped_value

    return inner
