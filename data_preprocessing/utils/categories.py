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

System_management_label2id = {
    'Utility': 1,
    'National grid': 1,
    '888': 0
}

Tariff_type_original2final = {
    'Fixed monthly fee': 'Fixed fee',
    'Utility estimates consumption': 'Consumption based',
    'Pay based on lights and appliances used': 'Consumption based',
    'No bill for electricity': 'No bill',
    'Other': 'Other'
}
Tariff_type_label2id = {
    'Fixed fee': 1,
    'Consumption based': 1,
    'No bill': 1,
    'Other': 0
}

Tariff_payment_method_original2final = {
    'Cash': 'Cash',
    'Pay at the bank/post office': 'Cash',
    'Pay at the utility office': 'Cash',
    'Vouchers/token/pre-paid card from local store': 'Pre-paid cards/tokens',
    'Credits using mobile money': 'Mobile credit'
}

Presence_appliance_group_3_label2id = {
    'Presence_incandescent_light_bulb': 15,
    'Presence_fluorescent_tube': 16,
    'Presence_compact_fluorescent_light_bulb': 17,
    'Presence_LED_light_bulb': 18,
    'Presence_radio/stereo': 20,
    'Presence_DVD_player': 21,
    'Presence_fan': 22,
    'Presence_refrigerator/freezer': 23,
    'Presence_microwave_oven': 24,
    'Presence_iron': 25,
    'Presence_washing_machine': 26,
    'Presence_sewing_machine': 27,
    'Presence_space_heater': 29,
    'Presence_traditional_water_heater': 30,
    'Presence_solar_based_water_heater': 31,
    'Presence_computer': 32,
    'Presence_kettle': 33,
    'Presence_smartphone_charger': 34,
    'Presence_regular_phone_charger': 35,
    'Presence_black&white_TV': 36,
    'Presence_color_TV': 37,
    'Presence_flat_color_TV': 38,
    'Presence_water_pump': 39
}

Presence_appliance_group_3_id2label = {i: key for key, i in Presence_appliance_group_3_label2id.items()}

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

Education_level_label2id = {
    'No schooling': 0,
    'Primary education': 1,
    'Lower secondary education': 1,
    'Post-secondary non-tertiary education': 1,
    "Bachelor's or equivalent level": 1,
    "Doctoral or equivalent level": 1,
    'Not elsewhere classified': 0
}


Male_Female_original2final = {
    "Male": "Male",
    "Female": "Female"
}

Marital_status_original2final = {
    'Married, Monogamous': 'Ongoing',
    'Never Married': 'Never started',
    'Widowed': 'Ended',
    'Married, Polygamous': 'Ongoing',
    'Cohabitating,Single Partner': 'Ongoing',
    'Separated': 'Ended',
    'Divorced': 'Ended',
    'Cohabitating, Multiple Partners': 'Ongoing'
}


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

