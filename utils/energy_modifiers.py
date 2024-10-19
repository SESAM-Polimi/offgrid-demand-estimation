from .constants import *
from .helpers import *


def get_connection_type(national_grid_question,
                        local_mini_grid_question,
                        solar_home_system_question, valid_answers):
    """
    Parameters
    ----------
    national_grid_question : str
        national grid question

    local_mini_grid_question : str
        local mini grid question

    solar_home_system_question : str
        solar home system question

    valid_answers : dict
        valid answers for the questions e.g.{'National grid': 'Yes', 'Local mini-grid': 'Yes', 'Solar Home System': 1}

    Returns
    -------
    Callable[[pd.Series], Any]
        The connection type of the dwelling
    """

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


def is_clean_fuel(clean_fuels, ref_question):
    """
    :param clean_fuels:  list of clean fuels
    :param ref_question re categorized main occupation
    """

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question, 'Fuel_usage'])

        max_usage = max(row['Fuel_usage'])
        pos_max = row['Fuel_usage'].index(max_usage)
        if row[ref_question][pos_max] in clean_fuels:
            return 'Yes'
        else:
            return 'No'

    return inner


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


def get_hours_available_electricity(national_grid_hours, local_mini_grid_hours, device_question, question_typicalmonth, valid_answer):
    """
    :arg national_grid_hours national grid hours question
    :arg local_mini_grid_hours local mini grid hours question
    :arg device_question device question for solar home system
    :arg question_typicalmonth question for typical month for solar home system
    :arg valid_answer valid answer for solar home system

    """

    def inner(row: pd.Series):
        result = np.nan
        # assert_many_columns_exists_in_row(row,
        #                                   ['Connection_type', national_grid_hours, local_mini_grid_hours,
        #                                    device_question])
        if row['Connection_type'] == NATIONAL_GRID:
            result = float(row[national_grid_hours][0])
        elif row['Connection_type'] == LOCAL_MINI_GRID:
            result = float(row[local_mini_grid_hours][0])

        elif row['Connection_type'] == SOLAR_HOME_SYSTEM:
            main_shs_dev = row[device_question]
            if main_shs_dev == valid_answer:
                result = float(row[question_typicalmonth][0])
        return result

    return inner
