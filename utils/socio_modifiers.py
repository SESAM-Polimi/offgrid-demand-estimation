import math
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


def extract_head_w_home_business_lsms(ref_question_1, ref_question_2, ref_question_3):
    """
    Extracts the head of the household with a home business. in LSMS datasets
    :param ref_question_1:  The reference question for the main occupation.
    :param ref_question_2:  The reference question for the employment status.
    :param ref_question_3:  The reference question for the age.
    :return:
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2, ref_question_3])

        result = ['No', np.nan]
        temp1 = 0
        temp2 = 0
        for i in range(len(row[ref_question_1])):
            if row[ref_question_1][i] == 1:
                if row[ref_question_2][i] == 1 or \
                        row[ref_question_2][i] == 2:
                    temp1 += 1
                elif is_nan(row[ref_question_2][i]):
                    temp2 += 1
        if temp1 > 0:
            result[0] = 'Yes'
            result[1] = 'Agri'
        elif temp1 == 0 and temp2 > 0:
            result[0] = np.nan
        if any(t == 1 for t in row[ref_question_3]):
            if result[0] == 'Yes':
                result[1] = 'Multiple'
            elif result[0] == 'No' or is_nan(result[0]):
                result[0] = 'Yes'
                result[1] = 'Non-agri'
        return result

    return inner


def extract_working_people(ref_question):
    def inner_extractor(row: pd.Series) -> float | int:
        if any(is_nan(t) for t in row[ref_question]):
            result = np.nan
            return result

        return sum(
            map(lambda x: (((x != 'Unemployed') and (isinstance(x, str))) or ((x != 2) and (not is_nan(x)))),
                row[ref_question]))

    return inner_extractor


def extract_socio_status_hhh(questionnaire, ref_question, hhh_relation_question,
                             hhh_relation_answer):
    '''
    Extracts the socio-economic status of the household head.

    Parameters:
    questionnaire (str): The name of the questionnaire.
    ref_question (str): The reference question for the main occupation.
    hhh_relation_question (str): The reference question for the household head relation.
    hhh_relation_answer (str): The answer for the household head relation.

    Returns:
    Callable[[pd.Series], Any]: The socio-economic status of the household head.
    '''

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
            assert_many_columns_exists_in_row(row, ["HHH_relation_pos", "sdd_indid"])
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


def extract_age_groups(ref_question, function_mode):
    """
    Extracts the number of people in the different age groups.

    Parameters:
    ref_question (str): The reference question for the age.
    function_mode (str): The mode of the function. It can be 'youngsters', 'adults', or 'elderly'.
    """

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


def extract_age_group_by_age_distribution(ref_question, age_distribution_norm: [float]):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question])
        temp = row[ref_question]
        return [x * temp for x in age_distribution_norm]

    return inner





def measurement_age(ref_question_1, ref_question_2, ref_question_solar_1, ref_question_solar_2):
    """
      Extracts the age of the connection based on the type of connection.

      Parameters:
      ref_question_1 (str): The reference question for the national grid connection.
      ref_question_2 (str): The reference question for the local mini grid connection.
      ref_question_solar_1 (str): The reference question for the solar home system.
      ref_question_solar_2 (str): The reference question for the type of solar home system.

      Returns:
      Callable([pd.Series], float]: The age of the connection if available, otherwise NaN.
      """

    def inner(row: pd.Series):
        result = np.nan
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2, 'Connection_type', ref_question_solar_1,
                                                ref_question_solar_2])
        try:
            connection_type = row['Connection_type']
            if is_nan(connection_type):
                return result
            if connection_type == NATIONAL_GRID:
                if row[ref_question_1][0] != ALWAYS_HAD_GRID and row[ref_question_1][0] != "Don't know":
                    result = float(row[ref_question_1][0])

            if connection_type == LOCAL_MINI_GRID:
                result = float(row[ref_question_2][0])
            if connection_type == SOLAR_HOME_SYSTEM:
                temp = []
                if type(row[ref_question_solar_2]) == list:
                    for i in range(len(row[ref_question_solar_1])):
                        if row[ref_question_solar_2][i] == 3 or \
                                row[ref_question_solar_2][
                                    i] == SOLAR_HOME_SYSTEM_SOLAR_PV:
                            temp.append(row[ref_question_solar_1][i])
                    if len(temp) > 0:
                        result = max(temp)
                else:
                    if row[ref_question_solar_2] == 3 or \
                            row[ref_question_solar_2] == SOLAR_HOME_SYSTEM_SOLAR_PV:
                        result = row[ref_question_solar_1]
            return result
        except Exception as e:
            print(e)
            raise AssertionError("Error in the data")

    return inner


def get_years_of_hhh_in_community_roster(hhh_relation_question,
                                         ref_question_1, ref_question_2, hhh_relation_answer):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2, hhh_relation_question])
        result = np.nan
        if row[hhh_relation_question].count(
                hhh_relation_answer) == 1:
            pos_head = row[hhh_relation_question].index(
                hhh_relation_answer)
            if row[ref_question_1][pos_head] != 99:
                result = row[ref_question_1][
                    pos_head]
            else:
                result = row[ref_question_2][
                    pos_head]

        return result

    return inner


def get_years_of_hhh_in_community_multi_section(hhh_relation_question,
                                                ref_question_1, ref_question_2, hhh_relation_answer):
    """
    Extracts the number of years the household head has lived in the community.
    :param hhh_relation_question:
    :param ref_question_1:
    :param ref_question_2:
    :param hhh_relation_answer:
    :return: modifier function to extract the number of years the household head has lived in the community.
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2, hhh_relation_question])
        result = np.nan
        pos_head = row[ref_question_2][0]
        if is_nan(pos_head):
            return result

        if is_nan(row[hhh_relation_question]):
            return np.nan
        if pos_head > len(row[hhh_relation_question]):
            return result

        if row[hhh_relation_question][pos_head - 1] == hhh_relation_answer:
            ref_question_1_value = row[ref_question_1][0]
            result = filtering(ref_question_1_value, 888,
                               111)

        return result

    return inner


def get_people_roster(ref_question):
    """
    Extracts the number of people in the roster.
    :param ref_question:
    :return:  modifier function to extract the number of people in the roster.
    """

    def inner(row: pd.Series):
        assert_column_exists_in_row(row, ref_question)
        return len(row[ref_question])

    return inner


def get_people_multi_question(hh_people_cluster):
    """
    Extracts the number of people using multi question from hh_people cluster.
    :param hh_people_cluster:
    :return:  modifier function to extract the number of people using multi question from hh_people cluster.
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, hh_people_cluster)
        result = 0
        for question in hh_people_cluster:
            result += row[question][0]
        return result

    return inner


def extract_relation_pos(ref_question_1, ref_question_2, answer):
    """
    Extracts the relation position of the household head.
    :param ref_question_1:  The reference question for the relation position.
    :param ref_question_2:  The reference question for the relation position.
    :param answer:  The answer for the relation position.
    :return: modifier function to extract the relation position of the household head.
    """

    def inner(row: pd.Series):
        result = np.nan
        for i in range(len(row[ref_question_1])):
            if row[ref_question_1][i] == answer:
                result = row[ref_question_2][i]
                return result
        return result

    return inner
