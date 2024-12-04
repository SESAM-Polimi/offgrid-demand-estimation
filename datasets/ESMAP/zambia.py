import os
import sys
import pandas as pd
import numpy as np

sys.path.append("../../")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from core.ODEDataset import ODEDataset
from utils import common_modifiers, dwelling_modifiers, socio_modifiers, finance_modifiers, appliances_modifiers, \
    geospatial, energy_modifiers

from utils.helpers import is_nan
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

Tariff_payment_frequency_original2final = {
    1: "Weekly",
    2: "Every 2 weeks",
    3: "Monthly",
    4: "Every 6 months",
    555: "Other"
}
Education_level_original2final = {
    1: "No schooling",
    2: "Primary education",
    3: "Lower secondary education",
    4: "Upper secondary education",
    5: "Post-secondary non-tertiary education",
    6: "Short-cycle tertiary education",
    7: "Bachelor's or equivalent level"
}
Main_occupation_original2final = {
    1: "Employee non-farm",
    2: "Employee farm",
    3: "Own-account worker non-farm",
    4: "Own-account worker non-farm",
    5: "Own-account worker farm",
    6: "Contributing family worker",
    7: "Worker not classifiable by status",
    8: "Worker not classifiable by status",
    9: "Unemployed",
    10: "Unemployed",
    11: "Unemployed",
    12: "Unemployed",
    555: "Worker not classifiable by status"
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
    9: 0,
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
    2: 0,
    3: 1,
    4: 1,
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
Dwelling_Toilet_Quality_original2final = {
    1: 0,
    2: 1,
    3: 1,
    4: 0,
    5: 1,
    6: 0,
    7: 0,
    555: 0
}
Ownership_motorized_vehicle_all_original2final = {
    1: 1,
    2: 1,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
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
    9: 0,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 0,
    15: 0,
    16: 0,
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
    9: 1,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0
}
System_management_original2final = {
    "National grid": "Utility",
    888: "888"
}

Province_raw_original2final = {
    1: "Central",
    2: "Copperbelt",
    3: "Eastern",
    4: "Luapula",
    5: "Lusaka",
    6: "Muchinga",
    7: "North-Western",
    8: "Northern",
    9: "Southern",
    10: "Western"
}

# %% Section A: Socio Data

section_a = ODEDataset("Zambia/Section A")
section_a.from_csv("../../playground/data/ESMAP/zambia/section a.csv", encoding='latin1'
                   ).group_by("HouseholdID")

section_a = section_a.new_feature("Age_HHH", socio_modifiers.extract_age_of_head("A5", "A4", 1))

section_a = section_a.new_feature("Education_level_HHH_raw",
                                  common_modifiers.categorize("A9", Education_level_original2final))
section_a = section_a.new_feature("Education_level_HHH", lambda x: x['Education_level_HHH_raw'][0])

section_a = section_a.new_feature("People_per_household", socio_modifiers.get_people_roster("A3"))

section_a = section_a.new_feature("Number_adults", lambda x: x['People_per_household'] * 0.539)

section_a = section_a.new_feature("Main_occupation",
                                  common_modifiers.categorize("A14", Main_occupation_original2final))

section_a = section_a.new_feature("Socio_status_HHH",
                                  socio_modifiers.extract_socio_status_hhh("zambia", 'Main_occupation',
                                                                           'A4', 1))

section_a = section_a.new_feature('HH_with_home_business_raw',
                                  socio_modifiers.extract_head_w_home_business('A19', 'Main_occupation',
                                                                               'A5', 1))
section_a = section_a.new_feature('HH_with_home_business', lambda x: x['HH_with_home_business_raw'][0])

section_a = section_a.select(
    ["HouseholdID", "Age_HHH", "Education_level_HHH", "Number_adults", "HH_with_home_business", "Socio_status_HHH"])

# %% Section B: Dwelling Data and GIS


express_sections = ODEDataset("Zambia/express sections")
express_sections.from_csv("../../playground/data/ESMAP/zambia/express sections.csv", encoding='latin1'
                          ).group_by("HouseholdID")

mtf_a1 = ODEDataset("Nigeria/mtf_ng_hh_sec_a1 helper")

mtf_a1.from_csv("../../playground/data/ESMAP/zambia/section a.csv", encoding='latin1'
                ).group_by("HouseholdID").select(["HouseholdID", "A4"])

express_sections = express_sections.merge(mtf_a1, "HouseholdID")

express_sections = express_sections.apply(common_modifiers.transform_list_int("B9"))
express_sections = express_sections.new_feature("Number_of_rooms", lambda  x : x['B9'][0])

dwelling_cols = [
    "B10",
    "B11",
    "B12",
    "B14",
    "B13_1",
    "A4",
    "B4",
    "B1"
]

for col in dwelling_cols:
    express_sections = express_sections.apply(
        common_modifiers.transform_list_int(col))

express_sections = express_sections.new_feature('Dwelling_wall',
                                                common_modifiers.categorize('B10',
                                                                            Dwelling_Wall_Quality_original2final))

express_sections = express_sections.new_feature("Dwelling_roof",
                                                common_modifiers.categorize("B11",
                                                                            Dwelling_Roof_Quality_original2final))

express_sections = express_sections.new_feature("Dwelling_floor",
                                                common_modifiers.categorize("B12",
                                                                            Dwelling_Floor_Quality_original2final))

express_sections = express_sections.new_feature("Dwelling_water",
                                                common_modifiers.categorize("B14",
                                                                            Dwelling_Water_Quality_original2final))

express_sections = express_sections.new_feature("Dwelling_toilet",
                                                common_modifiers.categorize("B13_1",
                                                                            Dwelling_Water_Quality_original2final))
express_sections = express_sections.new_feature("Dwelling_quality_index", dwelling_modifiers.dwelling_quality_index())

express_sections = express_sections.new_feature("Years_of_HHH_in_community",
                                                socio_modifiers.get_years_of_hhh_in_community_multi_section("A4", "B4",
                                                                                                            "B1", 1))

section_c_solar_devices = ODEDataset("Zambia/section_c_solar_devices")
section_c_solar_devices.from_csv("../../playground/data/ESMAP/zambia/section c solar devices.csv", encoding='latin1'
                                 ).group_by("HouseholdID")

express_sections = express_sections.merge(section_c_solar_devices, "HouseholdID")

connection_type_valid_answers = {constants.NATIONAL_GRID: 1, constants.LOCAL_MINI_GRID: 888,
                                 constants.SOLAR_HOME_SYSTEM: 1}

express_sections = express_sections.new_feature("Connection_type",
                                                energy_modifiers.get_connection_type('C2', 'C2',
                                                                                     'C138',
                                                                                     connection_type_valid_answers))

express_sections = express_sections.new_feature("Hours_available_electricity_not_filtered",
                                                energy_modifiers.get_hours_available_electricity('C28B',
                                                                                                 '-',
                                                                                                 'C164',
                                                                                                 'C140',
                                                                                                 3))

express_sections = express_sections.new_feature("Hours_available_electricity",
                                                energy_modifiers.filtering('Hours_available_electricity_not_filtered',
                                                                           888, -8))

express_sections = express_sections.new_feature("Measurement_age",
                                                socio_modifiers.measurement_age('C7', 'C46', 'C152', 'C140'))
express_sections = express_sections.new_feature("Tariff_payment_frequency_raw",
                                                common_modifiers.categorize("C13",
                                                                            Tariff_payment_frequency_original2final)).new_feature(
    "Tariff_payment_frequency",
    lambda x: x['Tariff_payment_frequency_raw'][0])

express_sections = express_sections.apply(common_modifiers.add_const_driver("GADM_level_0", "Zambia"))

express_sections = express_sections.new_feature("GADM_level_1_raw",
                                                common_modifiers.categorize("province", Province_raw_original2final))

express_sections = express_sections.new_feature("GADM_level_1", lambda x: x['GADM_level_1_raw'][0])

express_sections = express_sections.apply(common_modifiers.add_const_driver("GADM_level_2", np.nan))

gadm_level_1_df = pd.read_excel("../../playground/data/ESMAP/zambia/GADM_level_1.xlsx")
express_sections = express_sections.new_feature("Climate_zone_lev_1",
                                                geospatial.gis_info_by_gadm_level('Climate_majority',
                                                                                  gadm_level_1_df,
                                                                                  'GADM_level_1',
                                                                                  ))
express_sections = express_sections.apply(common_modifiers.add_const_driver("Climate_zone_lev_2", np.nan))

express_sections = express_sections.select([
    "HouseholdID", "Dwelling_quality_index", "Years_of_HHH_in_community", "Measurement_age",
    "Hours_available_electricity", "Tariff_payment_frequency",
    "Climate_zone_lev_1", "Climate_zone_lev_2",
    "Number_of_rooms"
])

# %% Section I: Finance Data

section_i = ODEDataset("Zambia/Section I")
section_i.from_csv("../../playground/data/ESMAP/zambia/section i.csv",
                   encoding='latin1').group_by("HouseholdID")
section_l = ODEDataset("Zambia/Section L")
section_l.from_csv("../../playground/data/ESMAP/zambia/section l.csv",
                   encoding='latin1').group_by("HouseholdID")

section_i = section_i.merge(section_l, "HouseholdID")

section_i = section_i.new_feature("Monthly_expenditure",
                                  finance_modifiers.expenditure_zambia())

# fuel_usage(data,source,questionnaire,'section i',hh,question,clusters)
section_i = section_i.new_feature("Fuel_usage",
                                  energy_modifiers.extract_fuel_usage(cooking_hrs_cluster))

section_i = section_i.new_feature("Clean_fuel",
                                  energy_modifiers.is_clean_fuel(constants.CLEAN_FUELS, 'I19A'))

section_i = section_i.select(["HouseholdID", "Monthly_expenditure", "Clean_fuel"])

# %% Section M: Ownership
section_m = ODEDataset("Zambia/Section M")
section_m.from_csv("../../playground/data/ESMAP/zambia/section m.csv",
                   encoding='latin1').group_by("HouseholdID")

section_m = section_m.apply(
    common_modifiers.transform_list_int("mitem"))

section_m = section_m.new_feature("Ownership_motorized_vehicle_all",
                                  common_modifiers.categorize("mitem",
                                                              Ownership_motorized_vehicle_all_original2final))


def get_ownership_vehicle(row: pd.Series):
    if any(t == 1 for t in row['Ownership_motorized_vehicle_all']):
        result = 'Yes'
    else:
        result = 'No'
    return result


section_m = section_m.new_feature("Ownership_motorized_vehicle",
                                  common_modifiers.find_any(
                                      'Ownership_motorized_vehicle_all', 1,
                                      'Yes', 'No'))

section_m = section_m.new_feature("Ownership_small_livestock_all",
                                  common_modifiers.categorize("mitem",
                                                              Ownership_small_livestock_all_original2final))
section_m = section_m.new_feature("Ownership_small_livestock",
                                  common_modifiers.find_any(
                                      'Ownership_small_livestock_all', 1,
                                      'Yes', 'No'))

section_m = section_m.new_feature("Ownership_large_livestock_all",
                                  common_modifiers.categorize("mitem",
                                                              Ownership_large_livestock_all_original2final))

section_m = section_m.new_feature("Ownership_large_livestock",
                                  common_modifiers.find_any(
                                      'Ownership_large_livestock_all', 1,
                                      'Yes', 'No'))

section_m = section_m.select(
    ["HouseholdID", "Ownership_motorized_vehicle", "Ownership_small_livestock", "Ownership_large_livestock"])

# %% Section N: Appliances
section_n = ODEDataset("Zambia/Section N")
section_n.from_csv("../../playground/data/ESMAP/zambia/section n.csv",
                   encoding='latin1').group_by("HouseholdID")

section_n = section_n.new_feature("Presence_smartphone_charger",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      25, 'nitem'))

section_n = section_n.new_feature("Presence_regular_phone_charger",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      26, "nitem"))

section_n = section_n.new_feature("Presence_phone_charger",
                                  common_modifiers.multi_unify_presence(
                                      ['Presence_smartphone_charger',
                                       'Presence_regular_phone_charger']))

section_n = section_n.new_feature("Presence_iron",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      11, "nitem"))

section_n = section_n.new_feature("Presence_freezer",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      15, "nitem"))

section_n = section_n.new_feature("Presence_refrigerator",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      9, "nitem"))

section_n = section_n.new_feature("Presence_refrigerator/freezer",
                                  common_modifiers.multi_unify_presence([
                                      'Presence_refrigerator',
                                      'Presence_freezer']))

section_n = section_n.new_feature("Presence_radio/stereo",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      6, 'nitem'))

section_n = section_n.new_feature("Presence_DVD_player",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      7, 'nitem'))

section_n = section_n.new_feature("Presence_fan",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      8, 'nitem'))

section_n = section_n.new_feature("Presence_black&white_TV",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      27, 'nitem'))

section_n = section_n.new_feature("Presence_color_TV",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B',
                                      28,
                                      'nitem'))

section_n = section_n.new_feature("Presence_flat_color_TV",
                                  appliances_modifiers.presence_appliances_long(
                                      'N1B', 29,
                                      'nitem'))

section_n = section_n.new_feature("Presence_TV",
                                  common_modifiers.multi_unify_presence(
                                      ['Presence_black&white_TV', 'Presence_color_TV',
                                       'Presence_flat_color_TV']))

section_n = section_n.select([
    "HouseholdID", "Presence_phone_charger", "Presence_iron", "Presence_TV", "Presence_refrigerator/freezer",
    "Presence_radio/stereo", "Presence_DVD_player", "Presence_fan"
])

# %% Merging all datasets
Zambia = section_a.merge(express_sections, "HouseholdID")
Zambia = Zambia.merge(section_i, "HouseholdID")
Zambia = Zambia.merge(section_m, "HouseholdID")
Zambia = Zambia.merge(section_n, "HouseholdID")

filename = "../../../playground/data/ESMAP/zambia/Zambia.csv"
Zambia.to_csv(filename)

print("All done", "exporting to ", filename)
