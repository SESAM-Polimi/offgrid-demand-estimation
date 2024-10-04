import os
import sys

sys.path.append("../")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from core.ODEDataset import ODEDataset

# MTF_HH_Roster
MTF_HH_Roster = ODEDataset("keyna/MTF_HH_Roster")
MTF_HH_Roster.from_csv("../playground/data/ESMAP/kenya/MTF_HH_Roster.csv").group_by("cluuq")

## Extracting Age data

MTF_HH_Roster.new_feature("Age_HHH",extract_age )


