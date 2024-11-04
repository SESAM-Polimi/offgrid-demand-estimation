from .constants import *
from .helpers import *


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



def get_dwelling_toilet_list(question_1, question_2, question_3, question_4):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [question_1, question_2, question_3, question_4])

        def get_value(col):
            value = row[col][0]
            if is_nan(value):
                return 0
            return value

        toilet_1 = get_value(question_1)
        toilet_2 = get_value(question_2)
        toilet_3 = get_value(question_3)
        toilet_4 = get_value(question_4)

        return [toilet_1, toilet_2, toilet_3, toilet_4]

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

