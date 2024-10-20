import os
import sys
from utils import common_modifiers
import numpy as np

sys.path.append("../")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from core.ODEDataset import ODEDataset

# %% Merge the datasets: Kenya, Zambia, and ESMAP
Kenya = ODEDataset("Kenya").from_csv("../playground/data/ESMAP/kenya/kenya.csv", index_col=0).apply(
    common_modifiers.rename({"cluuq": "ID"})).drop_columns(["Number_workers"])

Kenya = Kenya.apply(common_modifiers.add_const_driver("Tariff_payment_frequency", np.nan))
Zambia = ODEDataset("Zambia").from_csv("../playground/data/ESMAP/zambia/Zambia.csv", index_col=0).apply(
    common_modifiers.rename({"HouseholdID": "ID"}))

Nigeria = ODEDataset("Nigeria").from_csv("../playground/data/ESMAP/nigeria/Nigeria.csv", index_col=0).apply(
    common_modifiers.rename({"HH_ID": "ID"}))

# %% Save the merged dataset

ESMAP = Kenya.concat(Zambia).concat(Nigeria)
filename = "../playground/data/ESMAP/ESMAP.csv"
ESMAP.to_csv(filename)

print("ESMAP dataset saved to", filename)
