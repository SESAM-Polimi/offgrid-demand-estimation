#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys

sys.path.append("./")  # Adds higher directory to python modules path.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


# In[2]:


from core.ODEDataset import ODEDataset
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)
from utils import cleaning, constants, helpers


# In[3]:


src_path = "./playground/data/esmap_lsms-tanzania.csv"
missing_value = -1


# In[4]:


dataset = ODEDataset("combined")
dataset.from_csv(src_path)
dataset = dataset.select([
                             "ID",
                         ] + constants.DRIVERS_LIST + constants.PRESENCE_LIST)


# # Drivers

# ## Years_of_HHH_in_community

# In[5]:


dataset = dataset.apply(cleaning.fillna("Years_of_HHH_in_community", missing_value))
dataset = dataset.apply(cleaning.astype("Years_of_HHH_in_community", int))
dataset = dataset.new_feature("Years_of_HHH_in_community_missing",
                              cleaning.add_missing_flag("Years_of_HHH_in_community", missing_value))

dataset = dataset.apply(cleaning.standardize("Years_of_HHH_in_community"))
dataset.to_dataframe()[["Years_of_HHH_in_community", "Years_of_HHH_in_community_missing"]].head()


# ## Dwelling_quality_index
# 

# In[6]:


dataset = dataset.apply(cleaning.fillna("Dwelling_quality_index", missing_value))
dataset = dataset.apply(cleaning.astype("Dwelling_quality_index", int))
dataset = dataset.new_feature("Dwelling_quality_index_missing",
                              cleaning.add_missing_flag("Dwelling_quality_index", missing_value))
dataset = dataset.apply(cleaning.standardize("Dwelling_quality_index"))

dataset.to_dataframe()[["Dwelling_quality_index", "Dwelling_quality_index_missing"]].head()


# ## Hours_available_electricity

# In[7]:


dataset = dataset.apply(cleaning.fillna("Hours_available_electricity", missing_value))
dataset = dataset.apply(cleaning.astype("Hours_available_electricity", int))
dataset = dataset.new_feature("Hours_available_electricity_missing",
                              cleaning.add_missing_flag("Hours_available_electricity", missing_value))
dataset = dataset.apply(cleaning.standardize("Hours_available_electricity"))

dataset.to_dataframe()[["Hours_available_electricity", "Hours_available_electricity_missing"]].head()


# ## Measurement_age

# In[8]:


dataset = dataset.apply(cleaning.fillna("Measurement_age", missing_value))
dataset = dataset.apply(cleaning.replace_value("Measurement_age", -99, missing_value))
dataset = dataset.apply(cleaning.astype("Measurement_age", float))
dataset = dataset.new_feature("Measurement_age_missing", cleaning.add_missing_flag("Measurement_age", missing_value))
dataset = dataset.apply(cleaning.standardize("Measurement_age"))

dataset.to_dataframe()[["Measurement_age", "Measurement_age_missing"]].head()


# ## Monthly_expenditure

# In[9]:


dataset = dataset.apply(cleaning.fillna("Monthly_expenditure", missing_value))
dataset = dataset.apply(cleaning.astype("Monthly_expenditure", float))
dataset = dataset.apply(cleaning.replace_value("Monthly_expenditure", -99, missing_value))
dataset = dataset.new_feature("Monthly_expenditure_missing", cleaning.add_missing_flag("Monthly_expenditure", missing_value))
dataset = dataset.apply(cleaning.standardize("Monthly_expenditure"))

dataset.to_dataframe()[["Monthly_expenditure", "Monthly_expenditure_missing"]].head()


# ## Number_of_rooms

# In[10]:


dataset = dataset.apply(cleaning.fillna("Number_of_rooms", missing_value))
dataset = dataset.apply(cleaning.astype("Number_of_rooms", int))
dataset = dataset.new_feature("Number_of_rooms_missing", cleaning.add_missing_flag("Number_of_rooms", missing_value))
dataset = dataset.apply(cleaning.standardize("Number_of_rooms"))

dataset.to_dataframe()[["Number_of_rooms", "Number_of_rooms_missing"]].head()



# ## Climate_zone_lev_1

# In[11]:


dataset = dataset.apply(cleaning.fillna("Climate_zone_lev_1", missing_value))
dataset = dataset.apply(cleaning.astype("Climate_zone_lev_1", float))
dataset = dataset.new_feature("Climate_zone_lev_1_missing", cleaning.add_missing_flag("Climate_zone_lev_1", missing_value))

dataset = dataset.apply(cleaning.standardize("Climate_zone_lev_1"))

dataset.to_dataframe()[["Climate_zone_lev_1", "Climate_zone_lev_1_missing"]].head()



# ## Climate_zone_lev_2

# In[12]:


dataset = dataset.apply(cleaning.fillna("Climate_zone_lev_2", missing_value))
dataset = dataset.apply(cleaning.astype("Climate_zone_lev_2", float))

dataset = dataset.new_feature("Climate_zone_lev_2_missing", cleaning.add_missing_flag("Climate_zone_lev_2", missing_value))

dataset = dataset.apply(cleaning.standardize("Climate_zone_lev_2"))

dataset.to_dataframe()[["Climate_zone_lev_2", "Climate_zone_lev_2_missing"]].head()



# ## Age_HHH

# In[13]:


dataset = dataset.apply(cleaning.fillna("Age_HHH", missing_value))
dataset = dataset.apply(cleaning.astype("Age_HHH", int))
dataset = dataset.new_feature("Age_HHH_missing", cleaning.add_missing_flag("Age_HHH", missing_value))

dataset = dataset.apply(cleaning.standardize("Age_HHH"))
dataset.to_dataframe()[["Age_HHH", "Age_HHH_missing"]].head()


# ## HH_with_home_business

# In[14]:


dataset = dataset.apply(cleaning.fillna("HH_with_home_business", 'missing'))
dataset = dataset.apply(cleaning.astype("HH_with_home_business", str))

# add_one_hot_encoding
dataset = dataset.apply(cleaning.add_one_hot_encoding("HH_with_home_business"))


# ## Education_level_HHH

# In[15]:


dataset = dataset.apply(cleaning.fillna("Education_level_HHH", "Other"))
merged_categories = {
    'Other': "Not classified",
    "Not elsewhere classified": "Not classified",

    "No schooling": "No schooling",

    'Primary education': "Primary",

    'Upper secondary education': "Secondary",
    "Secondary education": "Secondary",
    'Lower secondary education': "Secondary",

    'Post-secondary non-tertiary education': "Tertiary",
    "Bachelor's or equivalent level": "Tertiary",
    "Short-cycle tertiary education": "Tertiary",
    "Doctoral or equivalent level": "Tertiary",
    "Master's or equivalent level": "Tertiary",

}
dataset = dataset.new_feature("Education_level_HHH",cleaning.merge_categories("Education_level_HHH", merged_categories))
dataset = dataset.apply(cleaning.add_one_hot_encoding("Education_level_HHH"))


# ## Socio_status_HHH

# In[16]:


dataset = dataset.apply(cleaning.fillna("Socio_status_HHH", "Other (not specified in Socio_status)"))

dataset = dataset.apply(cleaning.replace_value("Socio_status_HHH", "Other (not specified in Socio_status)", "Other"))

merged_categories = {
    'Own-account worker farm': "Worker",
    'Employee': "Worker",
    'Unemployed': "Unemployed",
    "Other": "Other",

    'Employee non-farm': "Worker",
    'Own-account worker non-farm': "Worker",
    'Contributing family worker': "Worker",
    'Worker not classifiable by status': "Worker",
    'Employee farm': "Worker",

    'Employer': "Employer",
}
dataset = dataset.new_feature("Socio_status_HHH",cleaning.merge_categories("Socio_status_HHH", merged_categories))
dataset = dataset.apply(cleaning.add_one_hot_encoding("Socio_status_HHH"))


#  ## Number_adults
# 

# In[17]:


dataset = dataset.apply(cleaning.fillna("Number_adults", -1))
dataset = dataset.apply(cleaning.astype("Number_adults", int))
dataset = dataset.new_feature("Number_adults_missing", cleaning.add_missing_flag("Number_adults", -1))

dataset.to_dataframe()[["Number_adults", "Number_adults_missing"]].head()


# ## Ownership_motorized_vehicle
# 

# In[18]:


dataset = dataset.apply(cleaning.replace_value("Ownership_motorized_vehicle", "1.0", 'Yes'))
dataset = dataset.apply(cleaning.replace_value("Ownership_motorized_vehicle", "0.0", 'No'))
dataset = dataset.apply(cleaning.fillna("Ownership_motorized_vehicle", 'missing'))
dataset = dataset.apply(cleaning.astype("Ownership_motorized_vehicle", str))

dataset = dataset.apply(cleaning.add_one_hot_encoding("Ownership_motorized_vehicle"))


# ## Ownership_small_livestock
# 

# In[19]:


dataset = dataset.apply(cleaning.replace_value("Ownership_small_livestock", "1.0", 'Yes'))
dataset = dataset.apply(cleaning.replace_value("Ownership_small_livestock", "0.0", 'No'))
dataset = dataset.apply(cleaning.fillna("Ownership_small_livestock", 'missing'))
dataset = dataset.apply(cleaning.astype("Ownership_small_livestock", str))

dataset = dataset.apply(cleaning.add_one_hot_encoding("Ownership_small_livestock"))


# ## Ownership_large_livestock
# 

# In[20]:


dataset = dataset.apply(cleaning.replace_value("Ownership_large_livestock", "1.0", 'Yes'))
dataset = dataset.apply(cleaning.replace_value("Ownership_large_livestock", "0.0", 'No'))
dataset = dataset.apply(cleaning.fillna("Ownership_large_livestock", 'missing'))
dataset = dataset.apply(cleaning.astype("Ownership_large_livestock", str))

dataset = dataset.apply(cleaning.add_one_hot_encoding("Ownership_large_livestock"))


# ## Clean_fuel
# 

# In[21]:


dataset = dataset.apply(cleaning.replace_value("Clean_fuel", "0", 'No'))
dataset = dataset.apply(cleaning.replace_value("Clean_fuel", "1", 'Yes'))
dataset = dataset.apply(cleaning.fillna("Clean_fuel", 'missing'))
dataset = dataset.apply(cleaning.astype("Clean_fuel", str))
dataset = dataset.apply(cleaning.add_one_hot_encoding("Clean_fuel"))


# ## Tariff_payment_frequency

# In[22]:


dataset = dataset.apply(cleaning.fillna("Tariff_payment_frequency", "not_classified"))
merged_categories = {
    'not_classified': "other",
    'Other': "other",
    'Monthly': "Monthly or More",
    'Every 2 weeks': "Weekly or More",
    'Weekly': "Weekly or More",
    'No bill': "other",
    'Every 6 months': "Monthly or More",
    'Every 3 months': "Monthly or More",
}
dataset = dataset.new_feature("Tariff_payment_frequency",cleaning.merge_categories("Tariff_payment_frequency", merged_categories))

dataset = dataset.apply(cleaning.add_one_hot_encoding("Tariff_payment_frequency"))


# In[ ]:





# # Appliances
# 

# In[23]:


PRESENCE_LIST = [
    'Presence_refrigerator/freezer', 'Presence_iron', 'Presence_fan',
    'Presence_DVD_player', 'Presence_radio/stereo',
    'Presence_phone_charger',
    'Presence_TV'
]

for p in PRESENCE_LIST:
    dataset = dataset.apply(cleaning.fillna(p, -1))
    value_counts = dataset.value_counts(p)
    print("Missing values for", p, value_counts[-1])


# In[24]:


dataset.preview()


# # Save the dataset

# In[37]:


from sklearn.model_selection import train_test_split

df = dataset.to_dataframe()
df = df.drop(columns=["ID"])
train_df, temp_df = train_test_split(df, test_size=0.4, random_state=412)
test_df, val_df = train_test_split(temp_df, test_size=0.5, random_state=412)


# In[38]:


print("Training")
for p in PRESENCE_LIST:
    value_counts = train_df.value_counts(p)
    print( value_counts)



# In[39]:


print("Validation")
for p in PRESENCE_LIST:
    value_counts = val_df.value_counts(p)
    print(value_counts)



# In[40]:


print("Testing")
for p in PRESENCE_LIST:
    value_counts = test_df.value_counts(p)
    print(value_counts)


# In[41]:


train_df.to_csv("./playground/data/normalized_train_set.csv", index=False)
val_df.to_csv("./playground/data/normalized_val_set.csv", index=False)
test_df.to_csv("./playground/data/normalized_test_set.csv", index=False)


# In[ ]:




