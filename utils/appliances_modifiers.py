from .helpers import *


# presence_appliances(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'m_m_3_group','888','17','string')

def presence_appliances_string(ref_question_1, ref_appliance):
    def inner(row: pd.Series):
        assert_column_exists_in_row(row, ref_question_1)

        if not is_nan(row[ref_question_1][0]):
            temp = row[ref_question_1][0].split()
            if any(t == ref_appliance for t in temp):
                return int(1)
            else:
                return int(0)

        return np.nan

    return inner


def presence_appliances_long(ref_question_1, ref_appliance, ref_question_2):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2])

        result = np.nan
        for i in range(len(row[ref_question_1])):
            if not is_nan(row[ref_question_1][i]):
                result = int(0)
                if row[ref_question_2][i] == ref_appliance and row[ref_question_1][i] >= 1:
                    result = int(1)
                    break
        return result

    return inner


def presence_appliances(ref_question_1, ref_appliance, ref_question_2):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [ref_question_1, ref_question_2])

        result = np.nan
        for i in range(len(row[ref_question_1])):
            result = int(0)
            if row[ref_question_1][i] == ref_appliance:
                result = int(1)
                break

        return result

    return inner
