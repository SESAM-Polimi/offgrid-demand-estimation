import pandas as pd
from typing import Callable, Any
import numpy as np
import math
from typing import Callable, Any
from .helpers import *


def categorize(feature: str, categories: dict):
    def inner(row):
        value = row[feature]
        if is_nan(value):
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
        all_nan = True
        for driver in drivers:
            if row[driver] == 1:
                return 1
            if not is_nan(row[driver]):
                all_nan = False
        if all_nan:
            return np.nan
        return 0

    return inner_unify_presence


def unify_presence(driver1: str, driver2: str) -> Callable:
    def inner_unify_presence(row: pd.Series) -> int:
        x = row[driver1]
        y = row[driver2]
        if x == 1 or y == 1:
            return 1
        
        if is_nan(x) and is_nan(y):
            return np.nan
        
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


def one_of_two(ref_question_1, ref_question_2):
    def inner(row: pd.Series):
        if is_nan(row[ref_question_1][0]):
            result = row[ref_question_2]
        else:
            result = row[ref_question_1]
        return result

    return inner


# These two functions replace the user_unification's function in the old code
def try_get_one(questions: [], raise_error: bool = False, not_found_value: Any = np.nan):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, questions)
        for question in questions:
            try:
                return row[question]
            except:
                continue

        if raise_error:
            raise ValueError('Value not found')
        return not_found_value

    return inner


def find_one(questions: [], predicate: Callable[[Any], bool],
             raise_error: bool = False, not_found_value: Any = np.nan):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, questions)
        for question in questions:
            if predicate(row[question]):
                return row[question]
        if raise_error:
            raise ValueError('Value not found')
        return not_found_value

    return inner


def select_multi_section_double_column_equal_to(ref_question_1, ref_answer, ref_question_2):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2])
        result = np.nan
        if type(row[ref_question_1]) == str or \
                row[ref_question_1] == int or \
                row[ref_question_1] == float:
            if row[ref_question_1] == ref_answer:
                result = [ref_question_2][0]
        if type(row[ref_question_1]) == list:
            for i in range(len(row[ref_question_1])):
                if row[ref_question_1][i] == ref_answer:
                    result = row[ref_question_2][i]
        return result

    return inner


def select_multi_section_double_column_equal_to_else_zero(ref_question_1, ref_answer, ref_question_2):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2])
        result = np.nan
        if type(row[ref_question_1]) == str or \
                row[ref_question_1] == int or \
                row[ref_question_1] == float:
            if row[ref_question_1] == ref_answer:
                result = row[ref_question_2][0]
            else:
                result = 0
        if type(row[ref_question_1]) == list:
            for i in range(len(row[ref_question_1])):
                if row[ref_question_1][i] == ref_answer:
                    result = row[ref_question_2][i]
            if is_nan(result):
                result = 0
        return result

    return inner


def single_column_assignment(ref_question, ref_answer, function_mode,
                             positive_output, negative_output):
    def inner(row: pd.Series):
        result = np.nan
        assert_column_exists_in_row(row, ref_question)

        temp = row[ref_question]
        if type(temp) == list:
            temp = temp[0]
        if function_mode == 'higher_than' and temp > ref_answer:
            result = positive_output
        if function_mode == 'equal_to' and temp == ref_answer:
            result = positive_output
        if function_mode == 'equal_to_else':
            if temp == ref_answer:
                result = positive_output
            else:
                result = negative_output
        if function_mode == 'not_empty':
            if not is_nan(temp):
                result = positive_output
        return result

    return inner


def extract_feature_by_position(ref_question, position_question):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question, position_question])

        temp = row[ref_question]
        if type(temp) != list:
            raise ValueError('The reference question is not a list')

        position = row[position_question]
        if position >= len(temp):
            raise ValueError('The position is out of range')

        if position == -1:
            return np.nan

        return temp[position]

    return inner


def is_in_list(ref_question, answers, positive_output, negative_output):
    def inner(row: pd.Series):
        assert_column_exists_in_row(row, ref_question)

        answer = row[ref_question]
        if type(answer) == list:
            answer = answer[0]

        if answer in answers:
            return positive_output
        else:
            return negative_output

    return inner
