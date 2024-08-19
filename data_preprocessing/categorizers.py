from lookup_tables import *
import pandas as pd

def build_climate_zone_features(src: pd.DataFrame):
    result = src.copy()
    cols = ["Climate_zone_lev_1", "Climate_zone_lev_2", "Climate_zone_lev_3"]
    for col in cols:
        result[col] = result[col].map(climate_zone_lev["label2id"]).fillna(0.0)
    return result


def build_urban_rural_features(src: pd.DataFrame):
    result = src.copy()
    result['Urban/rural'] = result['Urban/rural'].map(urban_rural["label2id"]).fillna(0.0)
    return result


def build_business_type_features(src: pd.DataFrame):
    result = src.copy()
    result['Type_of_business'] = result['Type_of_business'].map(business_type["label2id"]).fillna(0.0)
    return result


def build_system_management_features(src: pd.DataFrame):
    result = src.copy()
    result['System_management'] = result['System_management'].map(system_management["label2id"]).fillna(0.0)
    return result


# Connection_type
def build_connection_type_features(src: pd.DataFrame):
    result = src.copy()
    result['Connection_type'] = result['Connection_type'].map(connection_type["label2id"]).fillna(0.0)
    return result


def build_gender_features(src: pd.DataFrame):
    result = src.copy()
    result['Male/female_HHH'] = result['Male/female_HHH'].map(tariff_payment_frequency["label2id"]).fillna(0.0)
    return result


def build_tariff_payment_frequency_features(src: pd.DataFrame):
    result = src.copy()
    result['Tariff_payment_frequency'] = result['Tariff_payment_frequency'].map(
        tariff_payment_frequency["label2id"]).fillna(0.0)
    return result


def build_tariff_payment_method_features(src: pd.DataFrame):
    result = src.copy()
    result['Tariff_payment_method'] = result['Tariff_payment_method'].map(tariff_payment_method["label2id"]).fillna(0.0)
    return result


def build_social_status_features(src: pd.DataFrame):
    result = src.copy()
    result['Socio_status_HHH'] = result['Socio_status_HHH'].map(social_status["label2id"]).fillna(0.0)
    return result


def build_house_ownership_features(src: pd.DataFrame):
    result = src.copy()
    result['House_ownership_rental_free'] = result['House_ownership_rental_free'].map(
        house_ownership["label2id"]).fillna(0.0)
    return result


def build_martial_status_features(src: pd.DataFrame):
    result = src.copy()
    result['Marital_status_HHH'] = result['Marital_status_HHH'].map(martial_status["label2id"]).fillna(0.0)
    return result


def build_tariff_type_features(src: pd.DataFrame):
    result = src.copy()
    result['Tariff_type'] = result['Tariff_type'].map(tariff_type["label2id"]).fillna(0.0)
    return result

