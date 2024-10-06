import pandas as pd
import numpy as np
import math


# expenditure(data,source,questionnaire,'MTF_HH_Core_Survey','-','-',hh,clusters,1,1,1,'single_response')

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
        expenditure = 0
        for i in yearly_expenditure_cluster:
            if row[i][0] == 'Do not know' or row[i][0] == '111' or math.isnan(float(row[i][0])):
                expenditure = np.nan
                return expenditure
            expenditure += float(row[i][0])
            expenditure = expenditure / 12

        return expenditure

    return inner
