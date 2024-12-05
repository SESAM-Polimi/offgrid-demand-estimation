import pandas as pd
import numpy as np
import math

from .constants import NATIONAL_GRID, LOCAL_MINI_GRID
from .helpers import *


def calculate_expenditure_weekly(weekly_expenditure_cluster):
    def inner(row: pd.Series):
        expenditure = 0
        for i in weekly_expenditure_cluster:
            if row[i][0] == 'Do not know' or row[i][0] == '111' or math.isnan(float(row[i][0])):
                expenditure = np.nan
                return expenditure
            expenditure += float(row[i][0]) * 52

    return inner


def calculate_expenditure_monthly(monthly_expenditure_cluster):
    def inner(row: pd.Series):
        expenditure = 0
        for i in monthly_expenditure_cluster:
            if row[i][0] == 'Do not know':
                expenditure = np.nan
                return expenditure
            if i == 'l_l_17' and math.isnan(float(row[i][0])) == True:
                row[i][0] = 0
            if row[i][0] == '111' or math.isnan(
                    float(row[i][0])) == True:
                expenditure = np.nan
                return expenditure
            expenditure += float(row[i][0]) * 12

        return expenditure

    return inner


def calculate_expenditure_yearly(yearly_expenditure_cluster):
    def inner(row: pd.Series):
        result = 0
        for i in yearly_expenditure_cluster:
            if row[i][0] == 'Do not know' or row[i][0] == '111' or math.isnan(float(row[i][0])):
                result = np.nan
                return result
            result += float(row[i][0])
            result = result / 12

        return result

    return inner


def expenditure_roster():
    def inner(row: pd.Series):
        result = 0
        assert_many_columns_exists_in_row(row, [
            'L_1_13', 'L_consumption_purchased', 'L_14_22', 'L_expenditure',
            'L_23_36', 'L_expenditure_12months'
        ])

        pos_yes = [idx for idx, element in enumerate(row['L_1_13']) if
                   element == 1]
        for i in pos_yes:
            value = row['L_consumption_purchased'][i]
            if is_nan(value):
                continue
            if value == 888:
                result = np.nan
                return result

            result += value * 52

        pos_yes = [idx for idx, element in enumerate(row['L_14_22']) if
                   element == 1]
        for i in pos_yes:
            value = row['L_expenditure'][i]
            if value == 888:
                result = np.nan
                return result
            if not is_nan(value):
                result += value * 12

        pos_yes = [idx for idx, element in enumerate(row['L_23_36']) if
                   element == 1]
        for i in pos_yes:
            value = row['L_expenditure_12months'][i]
            if value == 888:
                result = np.nan
                return result
            if not is_nan(value):
                result += value

        result = result / 12

        return result

    return inner


def expenditure_zambia():
    def inner(row: pd.Series):
        expenditure = 0
        pos_yes = [idx for idx, element in enumerate(row['litem']) if
                   element in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]
        for i in pos_yes:
            if row['L2A'][i] != -8:
                expenditure += row['L2A'][i] * 52
        pos_yes = [idx for idx, element in enumerate(row['litem']) if
                   element in [14, 15, 16, 17, 18, 19, 20, 21, 22]]
        for i in pos_yes:
            if row['L2A'][i] != -8:
                expenditure += row['L2A'][i] * 12
        pos_yes = [idx for idx, element in enumerate(row['litem']) if
                   element in [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]]
        for i in pos_yes:
            if row['L2A'][i] != -8:
                expenditure += row['L2A'][i]
        expenditure = expenditure / 12

        return expenditure

    return inner


# for section in ['hh_sec_c', 'hh_sec_d', 'hh_sec_f', 'hh_sec_i', 'hh_sec_j1', 'hh_sec_k', 'hh_sec_l', 'hh_sec_k']:

def expenditure_multi_section(expenditure_yearly_cluster, expenditure_weekly_cluster, expenditure_monthly_cluster,
                              expenditure_multi_period_cluster):
    def inner(row: pd.Series):
        total = 0

        assert_many_columns_exists_in_row(row, expenditure_multi_period_cluster)
        assert_many_columns_exists_in_row(row, expenditure_weekly_cluster)
        assert_many_columns_exists_in_row(row, expenditure_monthly_cluster)
        assert_many_columns_exists_in_row(row, expenditure_yearly_cluster)

        for question in expenditure_yearly_cluster:
            try:
                for i in range(len(row[question])):
                    if not is_nan(row[question][i]):
                        temp = row[question][i] / 12
                        total += temp
            except:
                total = total
        for question in expenditure_monthly_cluster:
            try:
                for i in range(len(row[question])):
                    if not is_nan(row[question][i]):
                        temp = row[question][i]
                        total += temp
                    elif is_nan(row[question][i]):
                        expenditure = np.nan
                        return expenditure
            except:
                total = total
        for question in expenditure_weekly_cluster:
            try:
                for i in range(len(row[question])):
                    if not is_nan(row[question][i]):
                        temp = row[question][i] * 4
                        total += temp
                    elif question == 'hh_f03' and row['hh_f02'][i] == 1:
                        expenditure = np.nan
                        return expenditure
            except:
                total = total

        for question in expenditure_multi_period_cluster:
            for i in range(len(row[question])):
                if i in [0, 1, 2]:
                    if not is_nan(row[question][i]):
                        temp = row[question][i] * 4
                        total += temp
                else:
                    if not is_nan(row[question][i]):
                        temp = row[question][i]
                        total += temp

        return total

    return inner


def extract_electricity_expenditure_monthly(ref_question_1, ref_question_2):
    def inner(row: pd.Series):
        result = np.nan
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2, 'Connection_type'])
        if row['Connection_type'] == NATIONAL_GRID:
            result = float([ref_question_1][0])
        elif row['Connection_type'] == LOCAL_MINI_GRID:
            result = float([ref_question_2][0])
        return result

    return inner


def extract_electricity_expenditure_not_monthly(ref_question_1, ref_question_2):
    def inner(row: pd.Series):
        result = np.nan
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2])
        if type(row[ref_question_2][0]) == float or type(row[ref_question_2][0]) == int:
            if row[ref_question_1][0] == 'D2':
                result = row[ref_question_2][
                             0] * 15
            elif row[ref_question_1][0] == 'W':
                result = row[ref_question_2][
                             0] * 4
            elif row[ref_question_1][0] == 'W2' or \
                    row[ref_question_1][0] == 'M/2':
                result = row[ref_question_2][
                             0] * 2
            elif row[ref_question_1][0] == 'M':
                result = row[ref_question_2][0]
            elif row[ref_question_1][0] == 'M3':
                result = row[ref_question_2][
                             0] / 3
        return result

    return inner




