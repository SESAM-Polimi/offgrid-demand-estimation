from typing import Dict

import numpy as np

from .constants import *
from .helpers import *


def get_dwelling_toilet(question_1, question_2, question_3,
                        dwelling_toilet_quality_label2id):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, [question_1, question_2, question_3])

        def get_value(col):
            value = row[col][0]
            if is_nan(value):
                return np.nan
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


def dwelling_quality_index(dwelling_quality_cluster=None):
    if dwelling_quality_cluster is None:
        dwelling_quality_cluster = ["Dwelling_wall",
                                    "Dwelling_roof",
                                    "Dwelling_floor",
                                    "Dwelling_toilet",
                                    "Dwelling_water"
                                    ]

    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, dwelling_quality_cluster)
        temp = []
        for i in dwelling_quality_cluster:
            v = row[i]
            if type(v) == list:
                v = v[0]

            temp.append(v)

            return unify_quality(temp)

    return inner


def get_quality(questions: [str], quality_dict: Dict):
    def inner(row: pd.Series):
        assert_many_columns_exists_in_row(row, questions)

        temp = []
        for i in questions:

            v = row[i]
            if type(v) == list:
                v = v[0]

            if is_nan(v):
                temp.append(0)
            else:
                temp.append(get_value_from_dict(v, quality_dict))

        return unify_quality(temp)

    return inner


def unify_quality(values):
    if all(is_nan(v) for v in values):
        return np.nan

    if all(v == 0 for v in values):
        return 0

    if all(v == 1 for v in values):
        return 1

    tmp = []
    for v in values:
        if not is_nan(v):
            tmp.append(v)
        else:
            tmp.append(0)

    return np.average(tmp)
