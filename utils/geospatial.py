from .helpers import *
from .constants import *
import numpy as np
import pandas as pd


def calculate_gadm_name(name: str):
    result = name.lower()
    result = result.replace('-', ' ')
    return result.replace("'", "")


# GADM(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'cty','dist','div','subloc')
def get_gadm(
        gadm_level_1_df: pd.DataFrame,
        gadm_level_2_df: pd.DataFrame,
        gadm_level_3_df: pd.DataFrame,
        ref_question_lev_1,
        ref_question_lev_2,
        ref_question_lev_2_1,
        ref_question_lev_3,
        questionnaire: str
):
    """

    :param gadm_level_1_df:  GADM Level 1 data
    :param gadm_level_2_df:  GADM Level 2 data
    :param gadm_level_3_df:  GADM Level 3 data
    :param ref_question_lev_1: specify the reference question for GADM level 1 e.g cty
    :param ref_question_lev_2: specify the reference question for GADM level 2 e.g dist
    :param ref_question_lev_2_1: specify the reference question for GADM level 2_1 e.g div
    :param ref_question_lev_3: specify the reference question for GADM level 3 e.g subloc
    :param questionnaire:  specify the questionnaire e.g 'kenya' (Kenya has special implementation)
    :return: modifier to calculate GADM data
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_lev_1, ref_question_lev_2, ref_question_lev_2_1,
                                                ref_question_lev_3])

        result = [np.nan, np.nan, np.nan, np.nan]
        if not is_nan(row[ref_question_lev_1][0]):
            temp_1 = calculate_gadm_name(row[ref_question_lev_1][0])
            for i, row in gadm_level_1_df.iterrows():
                print(row["NAME_1"])
                temp_gadm_1 = calculate_gadm_name(row['NAME_1'])
                if temp_1 == temp_gadm_1:
                    result[0] = row['GID_1']
                    result[1] = row['NAME_1']
            if not is_nan(result[1]):
                temp_3 = np.nan
                temp_2 = np.nan
                temp_4 = np.nan
                if not is_nan(row[ref_question_lev_2][0]):
                    temp_2 = calculate_gadm_name(row[ref_question_lev_2][0])
                if ref_question_lev_2_1 != '' and not is_nan(row[ref_question_lev_2_1][0]):
                    temp_3 = calculate_gadm_name(
                        row[ref_question_lev_1][0].lower() + ' ' + row[ref_question_lev_2_1][0])
                    temp_4 = calculate_gadm_name(row[ref_question_lev_2_1][0])
                if not is_nan(temp_2) or not is_nan(temp_3) or not is_nan(temp_4):
                    for i, row in gadm_level_2_df.iterrows():
                        temp_gadm_1 = calculate_gadm_name(str(row['NAME_1']))
                        temp_gadm_2 = calculate_gadm_name(str(row['NAME_2']))
                        if temp_1 == temp_gadm_1 and (
                                temp_2 == temp_gadm_2 or temp_3 == temp_gadm_2 or temp_4 == temp_gadm_2):
                            result[0] = row['GID_2']
                            result[2] = row['NAME_2']
                            return result
                if ref_question_lev_2_1 != '' and not is_nan(
                        row[ref_question_lev_2_1][0]) and questionnaire == 'kenya':

                    for i, row in gadm_level_3_df.iterrows():
                        temp_gadm_3 = calculate_gadm_name(str(row['NAME_3']))
                        temp_gadm_2 = calculate_gadm_name(str(row['NAME_2']))
                        if temp_4 == temp_gadm_3:
                            result[0] = row['GID_2']
                            result[2] = row['NAME_2']
                            return result
                if ref_question_lev_3 != '' and not is_nan(
                        row[ref_question_lev_3][0]) and questionnaire == 'kenya':
                    temp_5 = calculate_gadm_name(row[ref_question_lev_3][0])
                    for i, row in gadm_level_3_df.iterrows():
                        temp_gadm_3 = calculate_gadm_name(str(row['NAME_3']))
                        temp_gadm_2 = calculate_gadm_name(str(row['NAME_2']))
                        if temp_5 == temp_gadm_3:
                            result[0] = row['GID_2']
                            result[2] = row['NAME_2']
                            return result
        return result

    return inner


def gis_info_by_gadm_level(variable, ref_question, df):
    def inner(row: pd.Series):
        result = np.nan
        if variable in GADM_variables:
            if not is_nan(row[ref_question]['Answer']):
                ref_question_gadm = ''
                if ref_question == 'GADM_level_1':
                    ref_question_gadm = 'NAME_1'
                elif ref_question == 'GADM_level_2':
                    ref_question_gadm = 'NAME_2'
                elif ref_question == 'GADM_level_3':
                    ref_question_gadm = 'NAME_3'
                for i in list(df[ref_question].keys()):
                    temp = row[ref_question]['Answer']
                    if ref_question == 'GADM_level_1':
                        if temp == df[ref_question][i][ref_question_gadm]['Answer'][0]:
                            result = df[ref_question][i][variable]['Answer'][0]
                            return result
                    elif ref_question == 'GADM_level_2':
                        if temp == df[ref_question][i][ref_question_gadm]['Answer'][0] and \
                                row['GADM_level_1']['Answer'] == \
                                df[ref_question][i]['NAME_1']['Answer'][0]:
                            result = df[ref_question][i][variable]['Answer'][0]
                            return result
                    elif ref_question == 'GADM_level_3':
                        if temp == df[ref_question][i][ref_question_gadm]['Answer'][0] and \
                                row['GADM_level_1']['Answer'] == \
                                df[ref_question][i]['NAME_1']['Answer'][0] and \
                                row['GADM_level_2']['Answer'] == \
                                df[ref_question][i]['NAME_2']['Answer'][0]:
                            result = df[ref_question][i][variable]['Answer'][0]
                            return result
            return result

    return inner


def gis_info_by_village_level(variable, df):
    def inner(row: pd.Series):
        result = np.nan
        vars = Village_variables + ['GADM_level_1', 'GADM_level_2', 'GADM_level_3']
        if variable in vars:
            if not is_nan(row['Township/Village']):
                for i in list(df['Village_GPS_info'].keys()):
                    temp = row['Township/Village']
                    if temp == df['Village_GPS_info'][i]['Name'][0]:
                        result = df['Village_GPS_info'][i][variable][0]
                        return result

        return result

    return inner
