import os
import sys
import pandas as pd
import numpy as np

sys.path.append("../")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from core.ODEDataset import ODEDataset
from utils import common_modifiers, dwelling_modifiers, socio_modifiers, finance_modifiers, appliances_modifiers, \
    geospatial, energy_modifiers

from utils import constants

# %% Clusters
cooking_hrs_cluster = [
    "I24",
    "I25",
    "I26",
    "I27",

]
Source_electricity_cluster = [
    "C43",
    "C136__3",
    "C182"
]
Dwelling_recategorization_cluster = [
    "B10",
    "B11",
    "B12",
    "B14"
]
loan_cluster = [
    "B20__1",
    "B20__2",
    "B20__3",
    "B20__4",
    "B20__5",
    "B20__6",
    "B20__7",
    "B20__8",
    "B20__9",
    "B20__10",
    "B20__11",
    "B20__12",
    "B20__13",
    "B20__555",
]

# %% Categories
Ownership_motorized_vehicle_all_original2final = {
    1: 1,
    2: 1,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    10: 0,
    11: 0,
    12: 0,
    14: 0,
    15: 0,
    17: 0
}
Ownership_small_livestock_all_original2final = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    10: 0,
    11: 1,
    12: 1,
    14: 1,
    15: 1,
    17: 0
}
Ownership_large_livestock_all_original2final = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 1,
    10: 1,
    11: 0,
    12: 0,
    14: 0,
    15: 0,
    17: 0
}
Dwelling_Wall_Quality_original2final = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 0,
    11: 1,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    555: 0
}
Dwelling_Roof_Quality_original2final = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    555: 0
}
Dwelling_Floor_Quality_original2final = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    555: 0
}
Dwelling_Water_Quality_original2final = {
    1: 1,
    3: 1,
    5: 1,
    6: 0,
    7: 0,
    8: 0,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    555: 0
}
Education_level_original2final = {
    0: 'No schooling',
    1: 'No schooling',
    2: 'No schooling',
    11: 'Primary education',
    12: 'Primary education',
    13: 'Primary education',
    14: 'Primary education',
    15: 'Primary education',
    16: 'Primary education',
    21: 'Lower secondary education',
    22: 'Lower secondary education',
    23: 'Lower secondary education',
    24: 'Upper secondary education',
    25: 'Upper secondary education',
    26: 'Upper secondary education',
    27: 'Primary education',
    28: 'Upper secondary education',
    31: 'Post-secondary non-tertiary education',
    32: 'Post-secondary non-tertiary education',
    33: 'Post-secondary non-tertiary education',
    34: 'Post-secondary non-tertiary education',
    41: 'Post-secondary non-tertiary education',
    42: "Bachelor's or equivalent level",
    43: "Master's or equivalent level",
    51: 'No schooling',
    52: 'Primary education',
    61: 'Not elsewhere classified'
}
Main_occupation_original2final = {
    1: 'Employee non-farm',
    2: 'Employee farm',
    3: 'Own-account worker non-farm',
    4: 'Own-account worker non-farm',
    5: 'Own-account worker farm',
    6: 'Contributing family worker',
    7: 'Worker not classifiable by status',
    8: 'Worker not classifiable by status',
    555: 'Worker not classifiable by status',
    9: 'Unemployed',
    10: 'Unemployed',
    11: 'Unemployed',
    12: 'Unemployed'
}
Tariff_payment_frequency_original2final = {
    1: "Weekly",
    2: "Every 2 weeks",
    3: "Monthly",
    4: "Every 6 months",
    555: "Other"
}

# %% mtf_ng_hh_sec_a1

mtf_ng_hh_sec_a1 = ODEDataset("Nigeria/mtf_ng_hh_sec_a1")
mtf_ng_hh_sec_a1.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_a1.csv", encoding='latin1'
                          ).group_by("HH_ID")

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Age_HHH", socio_modifiers.extract_age_of_head("A5", "A4", 1))

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Education_level_HHH_raw",
                                                common_modifiers.categorize("A9", Education_level_original2final))
mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Education_level_HHH", lambda x: x['Education_level_HHH_raw'][0])

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Number_adults", socio_modifiers.extract_age_groups("A5", "adults"))

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Main_occupation",
                                                common_modifiers.categorize("A14", Main_occupation_original2final))

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature("Socio_status_HHH",
                                                socio_modifiers.extract_socio_status_hhh("nigeria", 'Main_occupation',
                                                                                         'A4', 1))

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature('HH_with_home_business_raw',
                                                socio_modifiers.extract_head_w_home_business('A19', 'Main_occupation',
                                                                                             'A5', 1))
mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.new_feature('HH_with_home_business', lambda x: x['HH_with_home_business_raw'][0])

mtf_ng_hh_sec_a1 = mtf_ng_hh_sec_a1.select(
    ["HH_ID", "Age_HHH", "Education_level_HHH", "Number_adults", "HH_with_home_business", "Socio_status_HHH"])

mtf_ng_hh_sec_a1.to_dataframe().head()

# %% mtf_ng_hh_sec_b
mtf_ng_hh_sec_b = ODEDataset("Nigeria/mtf_ng_hh_sec_b")
mtf_ng_hh_sec_b.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_b.csv", encoding='latin1'
                         ).group_by("HH_ID")

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature('Dwelling_wall',
                                              common_modifiers.categorize('B10',
                                                                          Dwelling_Wall_Quality_original2final))
mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Dwelling_roof",
                                              common_modifiers.categorize("B11",
                                                                          Dwelling_Roof_Quality_original2final))

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Dwelling_floor",
                                              common_modifiers.categorize("B12",
                                                                          Dwelling_Floor_Quality_original2final))

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Dwelling_water",
                                              common_modifiers.categorize("B14",
                                                                          Dwelling_Water_Quality_original2final))

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Dwelling_toilet",
                                              dwelling_modifiers.get_dwelling_toilet_list("B13__2", "B13__3", "B13__5",
                                                                                          "B13__8",
                                                                                          ))

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Dwelling_quality_index", dwelling_modifiers.dwelling_quality_index)

mtf_a1 = ODEDataset("Nigeria/mtf_ng_hh_sec_a1 helper")

mtf_a1.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_a1.csv", encoding='latin1'
                ).group_by("HH_ID").select(["HH_ID", "A4"])

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.merge(mtf_a1, "HH_ID")

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.new_feature("Years_of_HHH_in_community",
                                              socio_modifiers.get_years_of_hhh_in_community_multi_section("A4", "B4",
                                                                                                          "B1", 1))

mtf_ng_hh_sec_b = mtf_ng_hh_sec_b.select([
    "HH_ID", "Dwelling_quality_index", "Years_of_HHH_in_community"
])

mtf_ng_hh_sec_b.to_dataframe().head()

# %% mtf_ng_hh_sec_l_30_days_expen
mtf_ng_hh_sec_l_30_days_expen = ODEDataset("Nigeria/mtf_ng_hh_sec_l_30_days_expen")
mtf_ng_hh_sec_l_30_days_expen.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_l_30_days_expen.csv",
                                       encoding='latin1').group_by("HH_ID")
mtf_ng_hh_sec_l_12_months_expen = ODEDataset("Nigeria/mtf_ng_hh_sec_l_12_months_expen")
mtf_ng_hh_sec_l_12_months_expen.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_l_12_months_expen.csv",
                                         encoding='latin1').group_by("HH_ID")
mtf_ng_hh_sec_l_consumption = ODEDataset("Nigeria/mtf_ng_hh_sec_l_consumption")
mtf_ng_hh_sec_l_consumption.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_l_consumption.csv",
                                     encoding='latin1').group_by("HH_ID")
mtf_ng_hh_sec_l_30_days_expen = mtf_ng_hh_sec_l_30_days_expen.merge(mtf_ng_hh_sec_l_12_months_expen, "HH_ID")
mtf_ng_hh_sec_l_30_days_expen = mtf_ng_hh_sec_l_30_days_expen.merge(mtf_ng_hh_sec_l_consumption, "HH_ID")

mtf_ng_hh_sec_l_30_days_expen = mtf_ng_hh_sec_l_30_days_expen.new_feature("Monthly_expenditure",
                                                                          finance_modifiers.expenditure_roster())

mtf_ng_hh_sec_l_30_days_expen = mtf_ng_hh_sec_l_30_days_expen.select(["HH_ID", "Monthly_expenditure"])

# %% mtf_ng_hh_sec_c
mtf_ng_hh_sec_c = ODEDataset("Nigeria/mtf_ng_hh_sec_c")
mtf_ng_hh_sec_c.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_c.csv", encoding='latin1').group_by("HH_ID")
mtf_ng_hh_sec_c_solar = ODEDataset("Nigeria/mtf_ng_hh_sec_c_solar")
mtf_ng_hh_sec_c_solar.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_c_solar.csv", encoding='latin1'
                               ).group_by("HH_ID")

mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.merge(mtf_ng_hh_sec_c_solar, "HH_ID")
connection_type_valid_answers = {constants.NATIONAL_GRID: 1, constants.LOCAL_MINI_GRID: 1,
                                 constants.SOLAR_HOME_SYSTEM: 1}
mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.new_feature("Connection_type",
                                              energy_modifiers.get_connection_type('C2', 'C43', 'C136__3',
                                                                                   connection_type_valid_answers))

mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.new_feature("Measurement_age",
                                              socio_modifiers.measurement_age('C7', 'C46', 'C153', 'C146'))

mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.new_feature("Hours_available_electricity",
                                              energy_modifiers.get_hours_available_electricity('C_28b', 'C68b', 'C169b',
                                                                                               'C146', 3))

mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.new_feature("Tariff_payment_frequency_raw", common_modifiers.categorize("C_13",
                                                                                                          Tariff_payment_frequency_original2final)).new_feature(
    "Tariff_payment_frequency",
    lambda x: x['Tariff_payment_frequency_raw'][0])

mtf_ng_hh_sec_c = mtf_ng_hh_sec_c.select(
    ["HH_ID", "Measurement_age", "Hours_available_electricity", "Tariff_payment_frequency"])

# %% mtf_ng_hh_sec_i_stove
mtf_ng_hh_sec_i_stove = ODEDataset("Nigeria/mtf_ng_hh_sec_i_stove")
mtf_ng_hh_sec_i_stove.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_i_stove.csv",
                               encoding='latin1').group_by("HH_ID")

# fuel_usage(data,source,questionnaire,'mtf_ng_hh_sec_i_stove',hh,question,clusters)
mtf_ng_hh_sec_i_stove = mtf_ng_hh_sec_i_stove.new_feature("Fuel_usage",
                                                          energy_modifiers.extract_fuel_usage(cooking_hrs_cluster))

mtf_ng_hh_sec_i_stove = mtf_ng_hh_sec_i_stove.new_feature("Clean_fuel",
                                                          energy_modifiers.is_clean_fuel(constants.CLEAN_FUELS, 'I19a'))
mtf_ng_hh_sec_i_stove = mtf_ng_hh_sec_i_stove.select(["HH_ID", "Clean_fuel"])

# %% NG_MTF_HH_SEC_0
NG_MTF_HH_SEC_0 = ODEDataset("Nigeria/NG_MTF_HH_SEC_0")
NG_MTF_HH_SEC_0.from_excel("../playground/data/ESMAP/nigeria/NG_MTF_HH_SEC_0.xlsx", ).group_by("HH_ID")
NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.apply(common_modifiers.add_const_driver("GADM_level_0", "Nigeria"))

gadm_level_1_df = pd.read_excel("../playground/data/ESMAP/nigeria/GADM_level_1.xlsx")
gadm_level_2_df = pd.read_excel("../playground/data/ESMAP/nigeria/GADM_level_2.xlsx")

NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("GADM_level_raw", geospatial.get_gadm(
    gadm_level_1_df,
    gadm_level_2_df,
    gadm_level_2_df,
    'state_id', 'lga', 'ward', '', 'nigeria'
))

NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("GADM_level_1", lambda x: x['GADM_level_raw'][1])
NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("GADM_level_2", lambda x: x['GADM_level_raw'][2])
NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("GADM_level_3", lambda x: np.nan)

NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("Climate_zone_lev_1",
                                              geospatial.gis_info_by_gadm_level('Climate_majority',
                                                                                gadm_level_1_df,
                                                                                'GADM_level_1',
                                                                                ))

NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.new_feature("Climate_zone_lev_2",
                                              geospatial.gis_info_by_gadm_level('Climate_majority',
                                                                                gadm_level_2_df,
                                                                                'GADM_level_2',
                                                                                ))
NG_MTF_HH_SEC_0 = NG_MTF_HH_SEC_0.select([
    "HH_ID", "Climate_zone_lev_1", "Climate_zone_lev_2"
])

# %% mtf_hh_sec_hh_asset_long
mtf_hh_sec_hh_asset_long = ODEDataset("Nigeria/mtf_hh_sec_hh_asset_long")
mtf_hh_sec_hh_asset_long.from_csv("../playground/data/ESMAP/nigeria/mtf_hh_sec_hh_asset_long.csv",
                                  encoding='latin1').group_by("HH_ID")

mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_motorized_vehicle_all",
                                                                common_modifiers.categorize("asset_list",
                                                                                            Ownership_motorized_vehicle_all_original2final))


def get_ownership_vehicle(row: pd.Series):
    if any(t == 1 for t in row['Ownership_motorized_vehicle_all']):
        result = 'Yes'
    else:
        result = 'No'
    return result


mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_motorized_vehicle",
                                                                common_modifiers.find_any(
                                                                    'Ownership_motorized_vehicle_all', 1,
                                                                    'Yes', 'No'))

mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_small_livestock_all",
                                                                common_modifiers.categorize("asset_list",
                                                                                            Ownership_small_livestock_all_original2final))

mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_large_livestock_all",
                                                                common_modifiers.categorize("asset_list",
                                                                                            Ownership_large_livestock_all_original2final))

mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_small_livestock",
                                                                common_modifiers.find_any(
                                                                    'Ownership_small_livestock_all', 1,
                                                                    'Yes', 'No'))

mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.new_feature("Ownership_large_livestock",
                                                                common_modifiers.find_any(
                                                                    'Ownership_large_livestock_all', 1,
                                                                    'Yes', 'No'))
mtf_hh_sec_hh_asset_long = mtf_hh_sec_hh_asset_long.select(
    ["HH_ID", "Ownership_motorized_vehicle", "Ownership_small_livestock", "Ownership_large_livestock"])

# %% mtf_ng_hh_sec_n_elec_asset
mtf_ng_hh_sec_n_elec_asset = ODEDataset("Nigeria/mtf_ng_hh_sec_n_elec_asset")
mtf_ng_hh_sec_n_elec_asset.from_csv("../playground/data/ESMAP/nigeria/mtf_ng_hh_sec_n_elec_asset.csv",
                                    encoding='latin1').group_by("HH_ID")

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_smartphone_charger",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        25, 'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_regular_phone_charger",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        26, "item_id"))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_phone_charger",
                                                                    common_modifiers.multi_unify_presence(
                                                                        ['Presence_smartphone_charger',
                                                                         'Presence_regular_phone_charger']))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_iron",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        11, "item_id"))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_freezer",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        15, "item_id"))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_refrigerator",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        9, "item_id"))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_refrigerator/freezer",
                                                                    common_modifiers.multi_unify_presence([
                                                                        'Presence_refrigerator',
                                                                        'Presence_freezer']))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_radio/stereo",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        6, 'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_DVD_player",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        7, 'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_fan",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        8, 'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_black&white_TV",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        27, 'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_color_TV",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset',
                                                                        28,
                                                                        'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_flat_color_TV",
                                                                    appliances_modifiers.presence_appliances_long(
                                                                        'own_asset', 29,
                                                                        'item_id'))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.new_feature("Presence_TV",
                                                                    common_modifiers.multi_unify_presence(
                                                                        ['Presence_black&white_TV', 'Presence_color_TV',
                                                                         'Presence_flat_color_TV']))

mtf_ng_hh_sec_n_elec_asset = mtf_ng_hh_sec_n_elec_asset.select([
    "HH_ID", "Presence_phone_charger", "Presence_iron", "Presence_TV", "Presence_refrigerator/freezer",
    "Presence_radio/stereo", "Presence_DVD_player", "Presence_fan"
])

# %% Merging
Nigeria = mtf_ng_hh_sec_a1.merge(mtf_ng_hh_sec_b, "HH_ID")
Nigeria = Nigeria.merge(mtf_ng_hh_sec_l_30_days_expen, "HH_ID")
Nigeria = Nigeria.merge(mtf_ng_hh_sec_c, "HH_ID")
Nigeria = Nigeria.merge(mtf_ng_hh_sec_i_stove, "HH_ID")
Nigeria = Nigeria.merge(NG_MTF_HH_SEC_0, "HH_ID")
Nigeria = Nigeria.merge(mtf_hh_sec_hh_asset_long, "HH_ID")
Nigeria = Nigeria.merge(mtf_ng_hh_sec_n_elec_asset, "HH_ID")

Nigeria.to_csv("../playground/data/ESMAP/nigeria/Nigeria.csv")
