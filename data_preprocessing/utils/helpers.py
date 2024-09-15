import numpy as np
import pandas as pd


def is_nan(value):
    return (
            str(value).lower() == "nan".lower()
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


def re_categorize(value, original2final: dict):
    result = np.nan
    if not is_nan(value):
        result = original2final[value]
    return result



