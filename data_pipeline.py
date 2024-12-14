import os
import sys

sys.path.append("./")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from core.ODEDataset import ODEDataset
from utils import cleaning
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE


def add_one_hot_encoding(dataset: ODEDataset):
    categorized_features = ['Education_level_HHH',
                            'Socio_status_HHH',
                            'Tariff_payment_frequency',
                            'HH_with_home_business',
                            'Ownership_motorized_vehicle',
                            'Ownership_small_livestock',
                            'Ownership_large_livestock',
                            'Clean_fuel',
                            ]
    for feature in categorized_features:
        dataset = dataset.apply(cleaning.add_one_hot_encoding(feature))
    return dataset


Features = [
    #    'Education_level_HHH',
    'Education_level_HHH_Doctoral or equivalent level',
    'Education_level_HHH_Lower secondary education',
    "Education_level_HHH_Master's or equivalent level",
    'Education_level_HHH_No schooling',
    'Education_level_HHH_Not elsewhere classified',
    'Education_level_HHH_Other',
    'Education_level_HHH_Post-secondary non-tertiary education',
    'Education_level_HHH_Primary education',
    'Education_level_HHH_Secondary education',
    'Education_level_HHH_Short-cycle tertiary education',
    'Education_level_HHH_Upper secondary education',
    # 'Socio_status_HHH',
    'Socio_status_HHH_Employee', 'Socio_status_HHH_Employee farm',
    'Socio_status_HHH_Employee non-farm', 'Socio_status_HHH_Employer',
    'Socio_status_HHH_Other', 'Socio_status_HHH_Own-account worker farm',
    'Socio_status_HHH_Own-account worker non-farm',
    'Socio_status_HHH_Unemployed',
    'Socio_status_HHH_Worker not classifiable by status',
    # 'Tariff_payment_frequency',
    'Tariff_payment_frequency_Every 3 months',
    'Tariff_payment_frequency_Every 6 months',
    'Tariff_payment_frequency_Monthly', 'Tariff_payment_frequency_No bill',
    'Tariff_payment_frequency_Other', 'Tariff_payment_frequency_Weekly',

    'HH_with_home_business_Yes',
    'HH_with_home_business_No',
    'HH_with_home_business_missing',

    'Ownership_motorized_vehicle_Yes',
    'Ownership_large_livestock_No',
    'Ownership_motorized_vehicle_missing',

    'Ownership_small_livestock_Yes',
    'Ownership_small_livestock_No',
    'Ownership_small_livestock_missing',

    'Ownership_large_livestock_Yes',
    'Ownership_large_livestock_No',
    'Ownership_large_livestock_missing',

    'Clean_fuel_Yes',
    'Clean_fuel_No',
    'Clean_fuel_missing',

    'Years_of_HHH_in_community',
    'Years_of_HHH_in_community_missing',

    'Dwelling_quality_index',
    'Dwelling_quality_index_missing',

    'Hours_available_electricity',
    'Hours_available_electricity_missing',

    'Measurement_age',
    'Measurement_age_missing',

    'Monthly_expenditure',
    'Monthly_expenditure_missing',

    'Number_of_rooms',
    'Number_of_rooms_missing',
    'Climate_zone_lev_1',
    'Climate_zone_lev_1_missing',

    'Climate_zone_lev_2',
    'Climate_zone_lev_2_missing',

    'Age_HHH',
    'Age_HHH_missing',

    'Number_adults',
    'Number_adults_missing'
]


def imbalance_class_sampling(x, y):
    """
        class imbalance sampling with SMOTE
        https://imbalanced-learn.org/stable/index.html
    """
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    return smote.fit_resample(x, y)


def create_dataset(output: str,
                   path="./playground/data/combined_dataset_cleaned.csv"):
    dataset = ODEDataset("combined_dataset_cleaned")
    dataset.from_csv(path)
    dataset = add_one_hot_encoding(dataset)
    dataset = dataset.apply(cleaning.remove_row(output, -1))
    return dataset.to_numpy(Features, [output])