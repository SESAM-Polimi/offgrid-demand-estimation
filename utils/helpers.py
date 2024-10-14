import numpy as np
import pandas as pd


def is_nan(value):
    return (
            value != value
            or str(value).lower() == "nan".lower()
            or value is None
            or value is np.nan
            or str(value).lower() == "NULL".lower()
            or str(value).lower() == "n/a".lower()
            or str(value).lower() == "na".lower()
            or str(value).lower() == "none".lower()
            or value is float("nan")
    )


def filtering(row: pd.Series, ref_question, wrong_answer_1, wrong_answer_2):
    result = row[ref_question]
    if (row[ref_question] == wrong_answer_1) or (row[ref_question] == wrong_answer_2):
        result = np.nan
    return result


def assert_column_exists_in_row(row: pd.Series, col):
    if col not in row.index:
        raise AssertionError(f"Column {col} is not present in the dataset")


def assert_many_columns_exists_in_row(row: pd.Series, cols):
    for col in cols:
        assert_column_exists_in_row(row, col)


def filtering(value, wrong_answer_1, wrong_answer_2):
    result = value
    if (value == wrong_answer_1) or (value == wrong_answer_2):
        result = np.nan
    return result
