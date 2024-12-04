ADULT_THRESHOLD = 65
YOUNG_THRESHOLD = 15
CLEAN_FUELS = ['LPG/cooking gas', 'Biogas', 'Electricity', 1, 5, 14, 16]
CLEAN_FUELS_Zambia = [1, 5, 7, 14]
BUSINESS = ['Contributing family worker', 'Own account worker non-farm', 'Own account worker farm']
CONNECTION = ['National grid', 'Local mini-grid', 'Solar Home System']
NATIONAL_GRID = 'National grid'
LOCAL_MINI_GRID = 'Local mini-grid'
SOLAR_HOME_SYSTEM = 'Solar Home System'
SOLAR_HOME_SYSTEM_SOLAR_PV = 'Solar home system (Solar PV system)'
ALWAYS_HAD_GRID = 'HH has always had grid connection'

Village_variables = ['Climate1', 'City_dist', 'Grid_dist', 'Latitude', 'Longitude', 'masl', 'Population']
GADM_variables = ['Climate_majority', 'Population_mean', 'Relative_wealth_index', 'masl_mean']

DRIVERS_LIST = ['Years_of_HHH_in_community',
                'Dwelling_quality_index', 'Hours_available_electricity',
                'Measurement_age', 'Monthly_expenditure', 'Number_of_rooms',
                'Climate_zone_lev_1', 'Climate_zone_lev_2',
                'Age_HHH', 'HH_with_home_business',
                'Education_level_HHH', 'Socio_status_HHH', 'Number_adults',
                'Ownership_motorized_vehicle', 'Ownership_small_livestock',
                'Ownership_large_livestock', 'Clean_fuel', 'Tariff_payment_frequency'
                ]

PRESENCE_LIST = [
    'Presence_refrigerator/freezer', 'Presence_iron', 'Presence_fan',
    'Presence_DVD_player', 'Presence_radio/stereo',
    'Presence_phone_charger',
    'Presence_TV'
]

# Dwelling quality

Dwelling_Wall_Quality = {
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

Dwelling_Roof_Quality = {
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

Dwelling_Floor_Quality = {
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

Dwelling_Toilet_Quality = {
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

Dwelling_Water_Quality = {
    'Piped water': 1,
    'Bore hole/ well': 1,
    'River/spring': 0,
    'Tanker/truck/vendor': 1,
    'Rain water': 1,
    'Lake/reservoir': 0,
    'Bottle water': 1,
    'Other': 0
}
