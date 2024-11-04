import os
import sys
import pandas as pd

sys.path.append("../../")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from core.ODEDataset import ODEDataset
from utils import common_modifiers, dwelling_modifiers, socio_modifiers, finance_modifiers, appliances_modifiers, \
    geospatial, energy_modifiers
from utils import constants

# %% Clusters

cooking_hrs_cluster = [
    "i_23_hrs_morning",
    "i_24_hrs_afternoon",
    'i_25_hrs_evening',
    'i_26_hrs_h2o'
]

monthly_expenditure_cluster = ['l_l_12',
                               'l_l_13',
                               'l_l_14',
                               'l_l_15',
                               'l_l_16',
                               'l_l_17',
                               'l_l_18',
                               'l_l_19']

# %% Categories
Main_occupation_original2final = {
    'Unemployed': 'Unemployed',
    'Student': 'Unemployed',
    'Wage Employee, Non-Farm': 'Employee non-farm',
    'Self-Employed Agriculture/Livestock': 'Own-account worker farm',
    'Casual/Day Laborer': 'Worker not classifiable by status',
    'Self-Employed Non-Farm-Business enterprise': 'Own-account worker non-farm',
    'Job Seeker': 'Unemployed',
    'Wage Employee, Farm': 'Employee farm',
    'Too old to work': 'Unemployed',
    'Self-Employed Non-Farm-Independent contractor,technician, professional, etc.': 'Own-account worker non-farm',
    'Retired/pensioner': 'Unemployed',
    'Assistance in family enterprise': 'Contributing family worker',
    'Other': 'Worker not classifiable by status',
    'Disabled': 'Unemployed',
    'Intern/free labor/voluntary work': 'Worker not classifiable by status'
}

Education_level_original2final = {
    'None': 'No schooling',
    'Primary': 'Primary education',
    'Secondary School': 'Lower secondary education',
    'Vocational/Technical/School- after completing primary education': 'Post-secondary non-tertiary education',
    'Vocational/Technical/School- after completing secondary education': 'Post-secondary non-tertiary education',
    'University': "Bachelor's or equivalent level",
    'Post-Grad': "Doctoral or equivalent level",
    'Other': 'Not elsewhere classified'
}

Dwelling_Wall_Quality_label2id = {
    'Blocks, plastered with cement': 1,
    'Stone and cement': 1,
    'Blocks, unplastered': 1,
    'Steel': 1,
    'Bricks': 1,
    'Mud bricks (traditional)': 0,
    'Wood and mud': 0,
    'Corrugated iron sheet': 0,
    'Chip wood': 0,
    'Parquet or polished wood': 0,
    'Wood only': 0,
    'Stone only': 0,
    'Wood and thatch': 0,
    'Stone and mud': 0,
    '0': 0,
    'Reed/bamboo': 0,
    'Asbestos': 0,
    'Other': 0,
    'Cargo container': 0
}

Dwelling_Roof_Quality_label2id = {
    'Corrugated iron sheet': 0,
    'Thatch': 0,
    'Concrete/Cement': 1,
    'Wood and mud': 0,
    'Bricks': 1,
    'Asbestos': 0,
    'Bamboo/Reed': 0,
    '0': 0,
    'Plastic canvas': 0,
    'Other': 0
}

Dwelling_Floor_Quality_label2id = {
    'Mud/Dung': 0,
    'Cement tiles': 1,
    'Ceramic/Marble tiles': 1,
    'Brick tiles': 1,
    'Plastic tiles': 1,
    'Wood planks': 1,
    'Parquet or polished wood': 1,
    'Cement screed': 1,
    '0': 0,
    'Other': 0,
    'Bamboo/Reed': 0
}

Dwelling_Toilet_Quality_label2id = {
    'Covered pit latrine': 1,
    'Uncovered pit latrine': 0,
    'Flush to sewage': 1,
    'Flush to septic tank': 1,
    'None': 1,
    'Community latrine': 0,
    'Pail / Bucket': 0,
    'Other, specify': 0,
    7.0: 0
}

Dwelling_Water_Quality_label2id = {
    'Piped water': 1,
    'Bore hole/ well': 1,
    'River/spring': 0,
    'Tanker/truck/vendor': 1,
    'Rain water': 1,
    'Lake/reservoir': 0,
    'Bottle water': 1,
    'Other': 0
}

Ownership_small_livestock_original2final = {
    'Camel': 0,
    'Cow/bull/calves': 0,
    'Goat': 1,
    'Horse/donkey': 0,
    'Other Animal': 0,
    'Pig': 1,
    'Sheep': 1
}

Ownership_large_livestock_original2final = {
    'Camel': 1,
    'Cow/bull/calves': 1,
    'Goat': 0,
    'Horse/donkey': 1,
    'Other Animal': 0,
    'Pig': 0,
    'Sheep': 0
}

Ownership_motorized_vehicle_original2final = {
    'Vehicle (Car, pickup truck, etc)': 1,
    'Bicycle': 0,
    'Domestic water pump': 0,
    'Motorcycle': 1,
    'Other equipment': 0,
    'Tractor': 0
}

# %% # MTF_HH_Roster


MTF_HH_Roster = ODEDataset("keyna/MTF_HH_Roster")
MTF_HH_Roster.from_csv("../../playground/data/ESMAP/kenya/MTF_HH_Roster.csv").group_by("cluuq")

MTF_HH_Roster = MTF_HH_Roster.new_feature("Age_HHH",
                                          socio_modifiers.extract_age_of_head('a_5_age', 'a_4_rel_hhh', 'Head'))

MTF_HH_Roster = MTF_HH_Roster.new_feature('Main_occupation',
                                          common_modifiers.categorize("a_14_main_occ", Main_occupation_original2final))

MTF_HH_Roster = MTF_HH_Roster.new_feature("HH_with_home_business",
                                          socio_modifiers.extract_head_w_home_business('a_19_hh_ent', 'Main_occupation',
                                                                                       'a_5_age', 'Yes'))

MTF_HH_Roster = MTF_HH_Roster.new_feature('Education_level_HHH',
                                          common_modifiers.categorize('a_9a_sch_lev', Education_level_original2final))

MTF_HH_Roster = MTF_HH_Roster.new_feature('Number_workers', socio_modifiers.extract_working_people('Main_occupation'))
MTF_HH_Roster = MTF_HH_Roster.new_feature('Socio_status_HHH',
                                          socio_modifiers.extract_socio_status_hhh('Kenya', 'Main_occupation',
                                                                                   'a_4_rel_hhh',
                                                                                   'Head'))

MTF_HH_Roster = MTF_HH_Roster.new_feature('Number_adults', socio_modifiers.extract_age_groups('a_5_age', 'adults'))
MTF_HH_Roster = MTF_HH_Roster.select(
    ['cluuq', 'Age_HHH', 'Number_workers', 'HH_with_home_business', "Education_level_HHH", 'Socio_status_HHH',
     'Number_adults'])

# %% # MTF_HH_Cooking_Data_Final

MTF_HH_Cooking_Data_Final = ODEDataset("keyna/MTF_HH_Cooking_Data_Final")
MTF_HH_Cooking_Data_Final.from_csv("../../playground/data/ESMAP/kenya/MTF_HH_Cooking_Data_Final.csv",
                                   encoding='ISO-8859-1').group_by("cluuq")

MTF_HH_Cooking_Data_Final = MTF_HH_Cooking_Data_Final.new_feature('Fuel_usage',
                                                                  energy_modifiers.extract_fuel_usage(
                                                                      cooking_hrs_cluster))

MTF_HH_Cooking_Data_Final = MTF_HH_Cooking_Data_Final.new_feature('Clean_fuel',
                                                                  energy_modifiers.is_clean_fuel(
                                                                      constants.CLEAN_FUELS,
                                                                      'i_18_a_1st_fuel'))

MTF_HH_Cooking_Data_Final = MTF_HH_Cooking_Data_Final.select(['cluuq', 'Clean_fuel'])

#%%  MTF_HH_Core_Survey
MTF_HH_Core_Survey = ODEDataset("keyna/MTF_HH_Core_Survey")
MTF_HH_Core_Survey.from_csv("../../playground/data/ESMAP/kenya/MTF_HH_Core_Survey.csv", encoding='ISO-8859-1').group_by(
    "cluuq")

MTF_HH_Solar_Roster = ODEDataset('kenya/MTF_HH_Solar_Roster').from_csv(
    "../../../playground/data/ESMAP/kenya/MTF_HH_Solar_Roster.csv", encoding='ISO-8859-1')
cls = [c for c in MTF_HH_Solar_Roster.get_columns() if c not in MTF_HH_Core_Survey.get_columns()]
cls.append("cluuq")
MTF_HH_Solar_Roster = MTF_HH_Solar_Roster.select(cls)
MTF_HH_Core_Survey = MTF_HH_Core_Survey.merge(MTF_HH_Solar_Roster, on='cluuq', how='left')

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature('Number_of_rooms',
                                                    lambda x: x['b_b_9'][0])

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature('Dwelling_wall',
                                                    common_modifiers.categorize('b_b_10',
                                                                                Dwelling_Wall_Quality_label2id))
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Dwelling_roof",
                                                    common_modifiers.categorize("b_b_11",
                                                                                Dwelling_Roof_Quality_label2id))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Dwelling_floor",
                                                    common_modifiers.categorize("b_b12",
                                                                                Dwelling_Floor_Quality_label2id))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Dwelling_water",
                                                    common_modifiers.categorize("b_b_14",
                                                                                Dwelling_Water_Quality_label2id))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Dwelling_toilet",
                                                    dwelling_modifiers.get_dwelling_toilet("b_b_13A", "b_b_13B",
                                                                                           "b_b_13C",
                                                                                           Dwelling_Toilet_Quality_label2id))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Dwelling_quality_index", dwelling_modifiers.dwelling_quality_index)

connection_type_valid_answers = {constants.NATIONAL_GRID: 'Yes', constants.LOCAL_MINI_GRID: 'Yes',
                                 constants.SOLAR_HOME_SYSTEM: 1}
connection_type_modifier = energy_modifiers.get_connection_type('c_c_2',
                                                                'c_c_38',
                                                                'c_c_q122_3',
                                                                connection_type_valid_answers)

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Connection_type", connection_type_modifier)

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature(
    "Hours_available_electricity",
    energy_modifiers.get_hours_available_electricity('c_c_25aii', 'c_c_25aii', 'c_127_device',
                                                     'c_c_147b_Typicalmonth', constants.SOLAR_HOME_SYSTEM_SOLAR_PV))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature('Measurement_age',
                                                    socio_modifiers.measurement_age('c_c_7', 'c_c_38', 'c_135_yrs',
                                                                                    'c_127_device'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature('Monthly_expenditure',
                                                    finance_modifiers.calculate_expenditure_monthly(
                                                        monthly_expenditure_cluster))
MTF_HH_Roster_relation_only = ODEDataset("keyna/MTF_HH_Roster_relation_only")
MTF_HH_Roster_relation_only.from_csv("../../playground/data/ESMAP/kenya/MTF_HH_Roster.csv").group_by("cluuq")
MTF_HH_Core_Survey = MTF_HH_Core_Survey.merge(MTF_HH_Roster_relation_only.select(['cluuq', 'a_4_rel_hhh']), on='cluuq',
                                              how='left')
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Years_of_HHH_in_community",
                                                    socio_modifiers.get_years_of_hhh_in_community_multi_section(
                                                        'a_4_rel_hhh', 'b_b_4', 'b_b_1', 'Head'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_smartphone_charger",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '34'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_regular_phone_charger",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '35'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_phone_charger", common_modifiers.multi_unify_presence(
    ['Presence_smartphone_charger', 'Presence_regular_phone_charger']))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_iron",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '25'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_refrigerator/freezer",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '23'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_radio/stereo",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '20'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_DVD_player",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '21'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_fan",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '22'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_black&white_TV",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '36'))
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_color_TV",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '37'))
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_flat_color_TV",
                                                    appliances_modifiers.presence_appliances_string('m_m_3_group',
                                                                                                    '38'))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Presence_TV", common_modifiers.multi_unify_presence(
    ['Presence_black&white_TV', 'Presence_color_TV', 'Presence_flat_color_TV']))

gadm_level_1_df = pd.read_excel("../../playground/data/ESMAP/kenya/GADM_level_1.xlsx")
gadm_level_2_df = pd.read_excel("../../playground/data/ESMAP/kenya/GADM_level_2.xlsx")
gadm_level_3_df = pd.read_csv("../../../playground/data/ESMAP/kenya/GADM_level_3.csv")

MTF_HH_Core_Survey = MTF_HH_Core_Survey.apply(common_modifiers.add_const_driver("GADM_level_0", "Kenya"))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("GADM_level_raw", geospatial.get_gadm(
    gadm_level_1_df,
    gadm_level_2_df,
    gadm_level_3_df,
    'cty', 'dist', 'div', 'subloc', 'kenya'
))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("GADM_level_1", lambda x: x['GADM_level_raw'][1])
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("GADM_level_2", lambda x: x['GADM_level_raw'][2])
MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("GADM_level_3", lambda x: x['GADM_level_raw'][3])

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Climate_zone_lev_1",
                                                    geospatial.gis_info_by_gadm_level('Climate_majority',
                                                                                      gadm_level_1_df,
                                                                                      'GADM_level_1',
                                                                                      ))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.new_feature("Climate_zone_lev_2",
                                                    geospatial.gis_info_by_gadm_level('Climate_majority',
                                                                                      gadm_level_2_df,
                                                                                      'GADM_level_2',
                                                                                      ))

MTF_HH_Core_Survey = MTF_HH_Core_Survey.select(['cluuq',
                                                'Years_of_HHH_in_community',
                                                'Dwelling_quality_index',
                                                'Hours_available_electricity',
                                                'Measurement_age',
                                                'Monthly_expenditure',
                                                'Number_of_rooms',
                                                "Climate_zone_lev_1",
                                                "Climate_zone_lev_2",
                                                'Presence_TV',
                                                'Presence_refrigerator/freezer',
                                                'Presence_iron',
                                                'Presence_fan',
                                                'Presence_DVD_player',
                                                'Presence_radio/stereo',
                                                'Presence_phone_charger',

                                                ])

# %%  # Asset_Data_Final
M1_Asset_Data_Final = ODEDataset('kenya/MTF_HH_Sec.M1_Asset_Data_Final').from_csv(
    "../../../playground/data/ESMAP/kenya/MTF_HH_Sec.M1_Asset_Data_Final.csv", encoding='ISO-8859-1')

M1_Asset_Data_Final = M1_Asset_Data_Final.group_by("cluuq")
M1_Asset_Data_Final = M1_Asset_Data_Final.new_feature("Ownership_motorized_vehicle_all",
                                                      common_modifiers.categorize('m_a_label',
                                                                                  Ownership_motorized_vehicle_original2final,
                                                                                  ))


def get_ownership_vehicle(row: pd.Series):
    if any(t == 1 for t in row['Ownership_motorized_vehicle_all']):
        result = 'Yes'
    else:
        result = 'No'
    return result


M1_Asset_Data_Final = M1_Asset_Data_Final.new_feature("Ownership_motorized_vehicle",
                                                      common_modifiers.find_any('Ownership_motorized_vehicle_all', 1,
                                                                                'Yes', 'No'))

M2_Asset_Data_Final = ODEDataset('kenya/MTF_HH_Sec.M2_Asset_Data_Final').from_csv(
    "../../../playground/data/ESMAP/kenya/MTF_HH_Sec.M2_Asset_Data_Final.csv", encoding='ISO-8859-1')

M2_Asset_Data_Final = M2_Asset_Data_Final.group_by("cluuq")

M2_Asset_Data_Final = M2_Asset_Data_Final.new_feature("Ownership_small_livestock_all",
                                                      common_modifiers.categorize("m_a_label",
                                                                                  Ownership_small_livestock_original2final,
                                                                                  ))

M2_Asset_Data_Final = M2_Asset_Data_Final.new_feature("Ownership_large_livestock_all",
                                                      common_modifiers.categorize('m_a_label',
                                                                                  Ownership_large_livestock_original2final,
                                                                                  ))

M2_Asset_Data_Final = M2_Asset_Data_Final.new_feature("Ownership_small_livestock",
                                                      common_modifiers.find_any('Ownership_small_livestock_all', 1,
                                                                                'Yes', 'No'))

M2_Asset_Data_Final = M2_Asset_Data_Final.new_feature("Ownership_large_livestock",
                                                      common_modifiers.find_any('Ownership_large_livestock_all', 1,
                                                                                'Yes', 'No'))

Asset_Data_Final = M1_Asset_Data_Final.merge(M2_Asset_Data_Final, on="cluuq")
Asset_Data_Final = Asset_Data_Final.select(
    ['cluuq', 'Ownership_motorized_vehicle', 'Ownership_small_livestock', 'Ownership_large_livestock'])

#%% Merge All

Kenya = MTF_HH_Core_Survey.merge(MTF_HH_Roster, on='cluuq')
Kenya = Kenya.merge(Asset_Data_Final, on='cluuq')
Kenya = Kenya.merge(MTF_HH_Cooking_Data_Final, on='cluuq')

filename = "../../../playground/data/ESMAP/kenya/kenya.csv"
Kenya.to_csv(filename)

print("Kenya done. File saved to", filename)
