import math
from typing import Callable, Any

import pandas as pd
from .constants import *

from .helpers import *

'''
:param ref_question re categorized main occupation
'''


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


def get_dwelling_toilet(question_1, question_2, question_3,
                        dwelling_toilet_quality_label2id):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [question_1, question_2, question_3])

        def get_value(col):
            value = row[col][0]
            if is_nan(value):
                return dwelling_toilet_quality_label2id['None']
            return dwelling_toilet_quality_label2id[value]

        toilet_1 = get_value(question_1)
        toilet_2 = get_value(question_2)
        toilet_3 = get_value(question_3)

        return [toilet_1 | toilet_2 | toilet_3]

    return inner


def dwelling_quality_index(row: pd.Series):
    dwelling_quality_cluster = ["Dwelling_wall",
                                "Dwelling_roof",
                                "Dwelling_floor",
                                "Dwelling_toilet",
                                "Dwelling_water"
                                ]
    assert_many_columns_exists_in_row(row, dwelling_quality_cluster)

    temp = []
    for i in dwelling_quality_cluster:
        if any(t == i for t in row.keys()):
            temp += [row[i][0]]
    if len(temp) == 5:
        return sum(temp) / len(temp)
    else:
        return np.nan


'''
:arg national_grid_question national grid question
:arg local_mini_grid_question local mini grid question
:arg solar_home_system_question solar home system question
:arg valid_answers valid answers for the questions e.g. {'National grid': 'Yes', 'Local mini-grid': 'Yes', 'Solar Home System': 1}
'''


def get_connection_type(national_grid_question,
                        local_mini_grid_question,
                        solar_home_system_question, valid_answers):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [national_grid_question, local_mini_grid_question,
                                                solar_home_system_question])
        connection_type = None
        if row[national_grid_question][0] == valid_answers[NATIONAL_GRID]:
            connection_type = NATIONAL_GRID
        elif row[local_mini_grid_question][0] == valid_answers[LOCAL_MINI_GRID]:
            connection_type = LOCAL_MINI_GRID
        elif row[solar_home_system_question][0] == valid_answers[SOLAR_HOME_SYSTEM]:
            connection_type = SOLAR_HOME_SYSTEM

        return connection_type

    return inner


'''
:arg national_grid_hours national grid hours question
:arg local_mini_grid_hours local mini grid hours question
:arg device_question device question for solar home system
:arg question_typicalmonth question for typical month for solar home system
'''


def get_hours_available_electricity(national_grid_hours, local_mini_grid_hours, device_question, question_typicalmonth):
    def inner(row: pd.Series):
        result = np.nan
        assert_many_columns_exists_in_row(row,
                                          ['Connection_type', national_grid_hours, local_mini_grid_hours,
                                           device_question])
        if row['Connection_type'] == NATIONAL_GRID:
            result = float(row[national_grid_hours][0])
        elif row['Connection_type'] == LOCAL_MINI_GRID:
            result = float(row[local_mini_grid_hours][0])

        elif row['Connection_type'] == SOLAR_HOME_SYSTEM:
            main_shs_dev = row[device_question]
            valid_answer = SOLAR_HOME_SYSTEM_SOLAR_PV
            if main_shs_dev == valid_answer:
                result = float(row[question_typicalmonth][0])
        return result

    return inner
