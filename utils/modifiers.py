import math
from typing import Callable, Any

import pandas as pd
from .constants import *

from .helpers import *


def extract_age_of_head(ref_question_1, head_relation_question, head_relation_answer):
    def inner_extractor(row: pd.Series) -> pd.Series:
        result = np.nan

        if row[head_relation_question].count(head_relation_answer) == 1:
            pos_head = row[head_relation_question].index(
                head_relation_answer)
            if row[ref_question_1][pos_head] != 888:
                result = row[ref_question_1][pos_head]

        return result

    return inner_extractor


# HH_w_home_business(data,source,questionnaire,'MTF_HH_Roster',hh,'a_19_hh_ent','Main_occupation','a_5_age','Yes')

#

def extract_head_w_home_business(ref_question_1, ref_question_2, ref_question_3, ref_answer):
    def inner(row: pd.Series) -> list[str | float | list[int]]:

        if ref_question_1 not in row.index:
            raise AssertionError(f"Column {ref_question_1} is not present in the dataset")
        if ref_question_2 not in row.index:
            raise AssertionError(f"Column {ref_question_2} is not present in the dataset")

        if ref_question_3 not in row.index:
            raise AssertionError(f"Column {ref_question_3} is not present in the dataset")

        result = ['No', np.nan]
        if any(t == ref_answer for t in row[ref_question_1]):
            result[0] = 'Yes'
            result[1] = [idx for idx, element in
                         enumerate(row[ref_question_1]) if
                         element == ref_answer]
        else:
            for i in range(len(row[ref_question_1])):
                if is_nan(row[ref_question_1][i]) and (
                        row[ref_question_2][i] != 'Unemployed' and not is_nan(row[ref_question_2][i])):
                    result[0] = np.nan
                    return result
                elif is_nan(row[ref_question_1][i]) and is_nan(row[ref_question_2][i]) and row[ref_question_3][i] >= 15:
                    result[0] = np.nan
                    return result
        return result

    return inner


def categorize(feature: str, categories: dict):
    def inner(row):
        value = row[feature]
        if value is None or value is np.nan:
            return np.nan

        if type(value) is list:
            result = []
            for v in value:
                if is_nan(v):
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


'''
:param ref_question re categorized main occupation
'''


def extract_working_people(ref_question):
    def inner_extractor(row: pd.Series) -> float | int:
        if any(is_nan(t) for t in row[ref_question]):
            result = np.nan
            return result

        return sum(
            map(lambda x: (((x != 'Unemployed') and (isinstance(x, str))) or ((x != 2) and (not is_nan(x)))),
                row[ref_question]))

    return inner_extractor


'''
:parameter 'ref_question is the re-categorized main occupation.'
:parameter 'HHH_relation_question is the name of the question which specifies the relation with the household head.'
:parameter 'HHH_relation_answer is the name of the answer which identifies the household head in HHH_relation_question.'
'''


# socio_status_HHH(data,source,questionnaire,'MTF_HH_Roster','Derived_variables',hh,'Main_occupation','a_4_rel_hhh','Head')
def extract_socio_status_hhh(questionnaire, ref_question, hhh_relation_question,
                             hhh_relation_answer):
    def inner(row: pd.Series):
        result = np.nan
        assert_many_columns_exists_in_row(row, [ref_question, hhh_relation_question])

        if questionnaire != 'Tanzania':
            if row[hhh_relation_question].count(
                    hhh_relation_answer) == 1:
                pos_head = row[hhh_relation_question].index(
                    hhh_relation_answer)
                result = row[ref_question][pos_head]

        if questionnaire == 'Tanzania':
            for i in range(len(row['sdd_indid'])):
                if row['sdd_indid'][i] == \
                        row['HHH_relation_pos']:
                    result = row[hhh_relation_question][i]
                    if result == 'Employee' and is_nan(
                            not row[ref_question][i]):
                        if row[ref_question][i] == 1:
                            result = 'Employee farm'
                        else:
                            result = 'Employee non-farm'
                    elif result == 'Employee' and is_nan(
                            row[ref_question][i]):
                        result = np.nan
        return result

    return inner


# age_groups(data,source,questionnaire,'MTF_HH_Roster',hh,'a_5_age','adults')
def extract_age_groups(ref_question, function_mode):
    def inner(row: pd.Series):
        result = 0
        if any(t == 888 for t in row[ref_question]) or any(
                math.isnan(t) for t in row[ref_question]):
            result = np.nan
            return result

        if function_mode == 'youngsters':
            result = len([i for i in row[ref_question] if i < YOUNG_THRESHOLD])
        elif function_mode == 'adults':
            result = len([i for i in row[ref_question] if YOUNG_THRESHOLD < i < ADULT_THRESHOLD])
        elif function_mode == 'elderly':
            result = len([i for i in row[ref_question] if i >= ADULT_THRESHOLD])

        return result

    return inner


# is_clean_fuel(data,source,questionnaire,'MTF_HH_Cooking_Data_Final','Derived_variables',hh,'i_18_a_1st_fuel')
def is_clean_fuel(clean_fuels, ref_question):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question, 'Fuel_usage'])

        max_usage = max(row['Fuel_usage'])
        pos_max = row['Fuel_usage'].index(max_usage)
        if row[ref_question][pos_max] in clean_fuels:
            return 'Yes'
        else:
            return 'No'

    return inner


# fuel_usage(data,source,questionnaire,'MTF_HH_Cooking_Data_Final',hh,question,clusters)

def extract_fuel_usage(cooking_hrs_cluster):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, cooking_hrs_cluster)
        result = []
        for j in range(len(row[cooking_hrs_cluster[0]])):
            result += [[]]
            for i in cooking_hrs_cluster:
                result[j] += [row[i][j]]
            result[j] = sum(result[j])

        return result

    return inner
