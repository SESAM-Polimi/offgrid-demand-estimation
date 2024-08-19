import numpy as np
from torch.utils.data import Dataset
import pandas as pd
import torch


class AppliancePredictionDataset(Dataset):
    def __init__(self, drivers_csv: str, appliance: np.ndarray):
        self.drivers_csv = drivers_csv
        self.appliance = appliance
        self._required_drivers = [
            "Income_of_household"
            , "Monthly_expenditure"
            , "People_per_household"
            , "Number_of_rooms"
            , "Distance_from_grid"
            , "Distance_from_city"
            , "Population"
            , "Population_density_lev_2"
            , "Population_density_lev_3"
            , "Relative_wealth_index_lev_2"
            , "Relative_wealth_index_lev_3"
            , "masl_lev_2"
            , "masl_lev_3"
            , "Measurement_age"
            , "Number_youngsters"
            , "Number_adults"
            , "Number_elderly"
            , "Monthly_electricity_expenditure"
            , "Size_of_business_employees"
            , "Education_level_HHH"
            , "Age_HHH"
            , "Price_candles"
            , "Price_kerosene"
            , "Price_charcoal"
            , "Seasonal_business"
            , "Age_of_business"
            , "Clean_fuel"
            , "Night_hours_study_children"
            , "Productive_uses_promotion"
            , "Capacity_building"
            , "Connection_fee"
            , "Pre-paid_tariff"
            , "HH_with_home_business"
            , "Access_to_credit"
            , "Street_lighting_present"
            , "Hours_available_electricity"
            , "Number_workers"
            , "Size_of_business_revenues"
            , "Years_of_HHH_in_community"
            , "Price_LPG"
            , "Price_firewood"
            , "Dwelling_quality_index"
            , "Land_owned"
            , "Monthly_electricity_consumption"
            , "Ownership_motorized_vehicle"
            , "Ownership_small_livestock"
            , "Ownership_large_livestock"
            , "Urban/rural_Rural"
            , "Urban/rural_Urban"
            # , "Climate_zone_lev_1_1.0"
            # , "Climate_zone_lev_1_2.0"
            # , "Climate_zone_lev_1_3.0"
            # , "Climate_zone_lev_1_4.0"
            # , "Climate_zone_lev_1_6.0"
            # , "Climate_zone_lev_1_9.0"
            # , "Climate_zone_lev_1_11.0"
            # , "Climate_zone_lev_1_12.0"
            # , "Climate_zone_lev_1_15.0"
            # , "Climate_zone_lev_1_Not_applicable"
            # , "Climate_zone_lev_2_1.0"
            # , "Climate_zone_lev_2_2.0"
            # , "Climate_zone_lev_2_3.0"
            # , "Climate_zone_lev_2_4.0"
            # , "Climate_zone_lev_2_6.0"
            # , "Climate_zone_lev_2_9.0"
            # , "Climate_zone_lev_2_11.0"
            # , "Climate_zone_lev_2_12.0"
            # , "Climate_zone_lev_2_15.0"
            # , "Climate_zone_lev_2_Not_applicable"
            # , "Climate_zone_lev_3_0.0"
            # , "Climate_zone_lev_3_3.0"
            # , "Climate_zone_lev_3_6.0"
            # , "Climate_zone_lev_3_11.0"
            # , "Climate_zone_lev_3_12.0"
            # , "Climate_zone_lev_3_Not_applicable"
            # , "System_management_Community"
            # , "System_management_Not_applicable"
            # , "System_management_Utility"
            # , "Respondent_category_Household"
            # , "Connection_type_Local mini-grid"
            # , "Connection_type_National grid"
            # , "Connection_type_Solar Home System"
            # , "Tariff_type_Consumption based"
            # , "Tariff_type_Fixed fee"
            # , "Tariff_type_No bill"
            # , "Tariff_type_Not_applicable"
            # , "Tariff_type_Other"
            # , "Tariff_payment_method_Cash"
            # , "Tariff_payment_method_Mobile credit"
            # , "Tariff_payment_method_Not_applicable"
            # , "Tariff_payment_method_Other"
            # , "Tariff_payment_method_Pre-paid cards/tokens"
            # , "Tariff_payment_frequency_Every 2 weeks"
            # , "Tariff_payment_frequency_Every 3 months"
            # , "Tariff_payment_frequency_Every 6 months"
            # , "Tariff_payment_frequency_Monthly"
            # , "Tariff_payment_frequency_Not_applicable"
            # , "Tariff_payment_frequency_Other"
            # , "Tariff_payment_frequency_Weekly"
            # , "Socio_status_HHH_Contributing family worker"
            # , "Socio_status_HHH_Employee farm"
            # , "Socio_status_HHH_Employee non-farm"
            # , "Socio_status_HHH_Employer"
            # , "Socio_status_HHH_Own-account worker farm"
            # , "Socio_status_HHH_Own-account worker non-farm"
            # , "Socio_status_HHH_Unemployed"
            # , "Socio_status_HHH_Worker not classifiable by status"
            # , "Male/female_HHH_Female"
            # , "Male/female_HHH_Male"
            # , "Marital_status_HHH_Ended"
            # , "Marital_status_HHH_Never started"
            # , "Marital_status_HHH_Ongoing"
            # , "House_ownership_rental_free_Owned"
            # , "House_ownership_rental_free_Rented"
            # , "House_ownership_rental_free_Used for free"
            # , "Type_of_business_A"
            # , "Type_of_business_B"
            # , "Type_of_business_C"
            # , "Type_of_business_D"
            # , "Type_of_business_E"
            # , "Type_of_business_F"
            # , "Type_of_business_G"
            # , "Type_of_business_H"
            # , "Type_of_business_I"
            # , "Type_of_business_K"
            # , "Type_of_business_L"
            # , "Type_of_business_Not_applicable"
            # , "Type_of_business_P"
            # , "Type_of_business_Q"
            # , "Type_of_business_R"
            # , "Type_of_business_S"
            # , "Type_of_business_T"
        ]
        self.raw_drivers_df = pd.read_csv(self.drivers_csv)
        self.validate(self.raw_drivers_df, self.appliance)
        self.prepare()

    def validate(self, drivers_df: pd.DataFrame, appliance: np.array):
        # Check if required columns exists
        missing_columns = []
        for col in self._required_drivers:
            if col not in drivers_df.columns:
                missing_columns.append(col)

        if len(missing_columns) > 0:
            raise Exception(" , ".join(missing_columns) + " are missing, but they are required!")

        if len(appliance.shape) != 1:
            raise Exception("Appliance must be one dimensional!")

        if len(drivers_df) != len(appliance):
            raise Exception(
                f"Number of examples mismatch,  drivers ({drivers_df.size}) != appliances ({appliance.size})")

    def prepare(self):
        self.drivers = self.raw_drivers_df[self._required_drivers]
        self.examples = self.drivers.to_numpy()
        self.targets = torch.Tensor(self.appliance)
        self.examples = torch.from_numpy(self.examples).float()

    def __len__(self):
        return len(self.drivers)

    def __getitem__(self, idx):
        return self.examples[idx], self.targets[idx]
