"""
Created on Thu Nov 11 12:48:56 2021

@author: loren
"""

import numpy as np
import math
import statistics

'Function to make our like easier'
def isNaN(string):
    return string != string

def NaN_to_string(data,source,questionnaire,section,hh,ref_question,string,function_mode):
        if function_mode == 'list':
            NaN_to_string = data[source][questionnaire][section][hh][ref_question]['Answer']
            if isNaN(data[source][questionnaire][section][hh][ref_question]['Answer'][0]) == True:
                NaN_to_string = [string]
        if function_mode == 'string':
            NaN_to_string = data[source][questionnaire][section][hh][ref_question]['Answer'][0]
            if isNaN(data[source][questionnaire][section][hh][ref_question]['Answer'][0]) == True:
                NaN_to_string = string
        return NaN_to_string

def is888(data,source,questionnaire,section,hh,ref_question):
    if ref_question == 888 or ref_question == '888':
        is888 = 888
    else:
        is888 = data[source][questionnaire][section][hh][ref_question]['Answer']
    return is888

def data_input(ref_answer):
    data_input = ref_answer
    return data_input

def copy(data,source,questionnaire,section,hh,ref_question_1):
    copy = data[source][questionnaire][section][hh][ref_question_1]['Answer']
    return copy

# first_of_list(data,source,questionnaire,'Chissinguana',hh,'P_light_bulb_simple_list')
def first_of_list(data,source,questionnaire,section,hh,ref_question_1):
    first_of_list = data[source][questionnaire][section][hh][ref_question_1]['Answer'][0]
    return first_of_list

def boolean_or(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3,function_mode):
    boolean_or = np.nan
    if function_mode == 'list':
        if any(isNaN(t) == False for t in data[source][questionnaire][section][hh][ref_question_1]['Answer']) or any(isNaN(t) == False for t in data[source][questionnaire][section][hh][ref_question_2]['Answer']) or any(isNaN(t) == False for t in data[source][questionnaire][section][hh][ref_question_3]['Answer']):
            if any(t == 'Yes' for t in data[source][questionnaire][section][hh][ref_question_1]['Answer']) or any(t== 'Yes' for t in data[source][questionnaire][section][hh][ref_question_2]['Answer']) or any(t == 'Yes' for t in data[source][questionnaire][section][hh][ref_question_3]['Answer']):
                boolean_or = 'Yes'
            else:
                boolean_or = 'No'
    if function_mode == 'element':
        if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer']) == False or isNaN(data[source][questionnaire][section][hh][ref_question_2]['Answer']) == False or isNaN(data[source][questionnaire][section][hh][ref_question_3]['Answer']) == False:
            if data[source][questionnaire][section][hh][ref_question_1]['Answer'] == 'Yes' or data[source][questionnaire][section][hh][ref_question_2]['Answer'] == 'Yes' or data[source][questionnaire][section][hh][ref_question_3]['Answer'] == 'Yes':
                boolean_or = 'Yes'
            else:
                boolean_or = 'No'
    return boolean_or

def one_of_two(data,source,questionnaire,section,hh,ref_question_1,ref_question_2):
    if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer'][0]) == True:
        one_of_two = data[source][questionnaire][section][hh][ref_question_2]['Answer']
    else: 
        one_of_two = data[source][questionnaire][section][hh][ref_question_1]['Answer']
    return one_of_two

CLEAN_FUELS = ['LPG/cooking gas', 'Biogas', 'Electricity',1,5,14,16]
CLEAN_FUELS_Zambia= [1,5,7,14]
BUSINESS = ['Contributing family worker', 'Own account worker non-farm', 'Own account worker farm']
CONNECTION = ['National grid','Local mini-grid','Solar Home System']

def fuel_usage(data,source,questionnaire,section,hh,question,clusters):
    
    fuel_usage = []
    for j in range(len(data[source][questionnaire][section][hh][clusters['cooking_hrs'][0]]['Answer'])):    
        fuel_usage += [[]]
        
        for i in clusters['cooking_hrs']:        
            fuel_usage[j] += [data[source][questionnaire][section][hh][i]['Answer'][j]]
        fuel_usage[j] = sum(fuel_usage[j])
        
    return fuel_usage


    # is_clean_fuel(data,source,questionnaire,'MTF_HH_Cooking_Data_Final','Derived_variables',hh,'i_18_a_1st_fuel')
def is_clean_fuel(data,source,questionnaire,section_1,section_2,hh,ref_question):
    
    max_usage = max(data[source][questionnaire][section_2][hh]['Fuel_usage']['Answer'])
    pos_max = data[source][questionnaire][section_2][hh]['Fuel_usage']['Answer'].index(max_usage)
    
    if questionnaire != 'zambia':
        if data[source][questionnaire][section_1][hh][ref_question]['Answer'][pos_max] in CLEAN_FUELS:
            check_clean = 'Yes'
        else:
            check_clean = 'No'
    else:
        if data[source][questionnaire][section_1][hh][ref_question]['Answer'][pos_max] in CLEAN_FUELS_Zambia:
            check_clean = 'Yes'
        else:
            check_clean = 'No'
    return check_clean
        
def HH_income(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,function_mode):
    'Function_mode should be either 0 if only one income question is present, 1 if 2 questions (e.g. a question...'
    'asking about income coming from secondary activities.'
    
    HH_income = 0
    if any(t == 888 or t == 111 or t == 555 for t in data[source][questionnaire][section][hh][ref_question_1]['Answer']) or any(t == 888 or t == 111 or t == 555 for t in data[source][questionnaire][section][hh][ref_question_2]['Answer']) or all(math.isnan(t) for t in data[source][questionnaire][section][hh][ref_question_1]['Answer']):
        HH_income = np.nan
        return HH_income
    
    for i in range(len(data[source][questionnaire][section][hh][ref_question_1]['Answer'])):
        if ((math.isnan(data[source][questionnaire][section][hh][ref_question_1]['Answer'][i]) == False) and (data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] != 888 or data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] != 111)):
            HH_income += data[source][questionnaire][section][hh][ref_question_1]['Answer'][i]
    if function_mode == 1:
        for i in range(len(data[source][questionnaire][section][hh][ref_question_2]['Answer'])):
            if ((math.isnan(data[source][questionnaire][section][hh][ref_question_2]['Answer'][i]) == False) and (data[source][questionnaire][section][hh][ref_question_2]['Answer'][i] != 888 or data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] != 111)):
                HH_income += data[source][questionnaire][section][hh][ref_question_2]['Answer'][i]
    return HH_income

def HH_people(data,source,questionnaire,section,hh,ref_question,function_mode,clusters):
    HH_people = np.nan
    
    if function_mode == 'roster':
        HH_people = len(data[source][questionnaire][section][hh][ref_question]['Answer'])
    
    if function_mode == 'multi_question':
        temp = 0
        for question in clusters['HH_people_cluster']:
            temp += data[source][questionnaire][section][hh][question]['Answer'][0]
        HH_people = temp
    return HH_people

# re_categorization(data,source,questionnaire,'Derived_variables',hh,'Connection_type','-','-',map_cat,'System_management',clusters)
def re_categorization(data,source,questionnaire,section,hh,ref_question,HHH_relation_question,HHH_relation_answer,map_cat,derived_variables_cat,clusters):
    'ref_question is the question to be re-categorized.'
    'HHH_relation_question is the name of the question which specifies the relation with the household head.'
    'HHH_relation_answer is the name of the answer which identifies the household head in HHH_relation_question.'
    
    if data[source][questionnaire][section][hh][ref_question]['Cluster'] == 'HHH_cluster' or data[source][questionnaire][section][hh][ref_question]['Cluster'] == 'Price_alternative_cluster':
        re_categorization = np.nan
        if data[source][questionnaire][section][hh][HHH_relation_question]['Answer'].count(HHH_relation_answer)==1:
            pos_head = data[source][questionnaire][section][hh][HHH_relation_question]['Answer'].index(HHH_relation_answer)
            for i in range(len(map_cat[derived_variables_cat]['Final_cat'])):
                if data[source][questionnaire][section][hh][ref_question]['Answer'][pos_head]== map_cat[derived_variables_cat]['Original_cat'][i]:
                    re_categorization = map_cat[derived_variables_cat]['Final_cat'][i]
        return re_categorization
    elif data[source][questionnaire][section][hh][ref_question]['Cluster'] == 'Dwelling_recategorization_cluster' or data[source][questionnaire][section][hh][ref_question]['Cluster'] == 'Single_answer_cluster':
        re_categorization = np.nan
        for i in range(len(map_cat[derived_variables_cat]['Final_cat'])):
            if data[source][questionnaire][section][hh][ref_question]['Answer'][0] == map_cat[derived_variables_cat]['Original_cat'][i]:
                re_categorization = map_cat[derived_variables_cat]['Final_cat'][i]
        return re_categorization
    
    elif data[source][questionnaire][section][hh][ref_question]['Cluster'] == 'Single_question_cluster':
        re_categorization = np.nan
        for i in range(len(map_cat[derived_variables_cat]['Final_cat'])):
            if data[source][questionnaire][section][hh][ref_question]['Answer'] == map_cat[derived_variables_cat]['Original_cat'][i]:
                re_categorization = map_cat[derived_variables_cat]['Final_cat'][i]
        return re_categorization
    else:
        re_categorization= []
        for j in range(len(data[source][questionnaire][section][hh][ref_question]['Answer'])):
            re_categorization.append(np.nan)
            for i in range(len(map_cat[derived_variables_cat]['Final_cat'])):
                    if data[source][questionnaire][section][hh][ref_question]['Answer'][j] == map_cat[derived_variables_cat]['Original_cat'][i]:
                        re_categorization[j] = map_cat[derived_variables_cat]['Final_cat'][i]              
        return re_categorization

# age_HHH(data,source,questionnaire,'MTF_HH_Roster',hh,'a_5_age','a_4_rel_hhh','Head')
def age_HHH(data,source,questionnaire,section,hh,ref_question_1,HHH_relation_question,HHH_relation_answer):
    'ref_question is the question about age of family member.'
    'HHH_relation_question is the name of the question which specifies the relation with the household head.'
    'HHH_relation_answer is the name of the answer which identifies the household head in HHH_relation_question.'
    
    age_HHH= np.nan
    
    if data[source][questionnaire][section][hh][HHH_relation_question]['Answer'].count(HHH_relation_answer)==1:
        pos_head = data[source][questionnaire][section][hh][HHH_relation_question]['Answer'].index(HHH_relation_answer)
        if data[source][questionnaire][section][hh][ref_question_1]['Answer'][pos_head] != 888:
            age_HHH = data[source][questionnaire][section][hh][ref_question_1]['Answer'][pos_head]
    
    return age_HHH

def age_groups(data,source,questionnaire,section,hh,ref_question,function_mode):
    'Function_mode can be one from: youngsters,adults,elderly depending on the envisaged age group'
    
    age_groups = 0
    if any(t == 888 for t in data[source][questionnaire][section][hh][ref_question]['Answer']) or any(math.isnan(t) for t in data[source][questionnaire][section][hh][ref_question]['Answer']):
        age_groups = np.nan
        return age_groups

    if function_mode == 'youngsters':
        age_groups = sum(map(lambda x : x<15, data[source][questionnaire][section][hh][ref_question]["Answer"]))
    elif function_mode == 'adults':
        age_groups = sum(map(lambda x : 65>x>14, data[source][questionnaire][section][hh][ref_question]["Answer"]))
    elif function_mode == 'elderly':
        age_groups = sum(map(lambda x : x>64, data[source][questionnaire][section][hh][ref_question]["Answer"]))
        
    return age_groups

def age_groups_extraction(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,start,finish,function_mode):
    age_groups_extraction = np.nan
    distr = [0,0]
    
    if section_1 == 'Derived_variables':
        temp = data[source][questionnaire][section_1][hh][ref_question_1]['Answer']
    else: temp = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0]
    
    if section_2 == 'Derived_variables':
        pop = data[source][questionnaire][section_2][hh]['GADM_level_0']['Answer']
    else: pop = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0]
    
    if isNaN(temp) == True:
        age_groups_extraction = [np.nan, np.nan]
        return age_groups_extraction

    if isNaN(pop) == False:
        for i in range(len(np.arange(start,finish+1))):
            if function_mode == 'youngsters_adults':
                if start+i < 15:
                    distr[0] += data[source][questionnaire][pop][start+i]['Distr']['Answer'][0]
                else: distr[1] += data[source][questionnaire][pop][start+i]['Distr']['Answer'][0]
            if function_mode == 'adults_elderly':
                if start+i < 65:
                    distr[0] += data[source][questionnaire][pop][start+i]['Distr']['Answer'][0]
                else: distr[1] += data[source][questionnaire][pop][start+i]['Distr']['Answer'][0]      
        distr_norm = [x/sum(distr) for x in distr]
        age_groups_extraction = [x*temp for x in distr_norm]
    else:
        age_groups_extraction = [np.nan, np.nan]
    return age_groups_extraction

# HH_working_people(data,source,questionnaire,'Derived_variables',hh,'Main_occupation')
def HH_working_people(data,source,questionnaire,section,hh,ref_question):
     'ref_question is the re-categorized main occupation.'
     
     HH_working_people = 0
     if any(isNaN(t) for t in data[source][questionnaire][section][hh][ref_question]['Answer']):
         HH_working_people = np.nan
         return HH_working_people
     
     HH_working_people = sum(map(lambda x : (((x != 'Unemployed') and (isinstance(x, str))) or ((x != 2) and (isNaN(x) == False))), data[source][questionnaire][section][hh][ref_question]["Answer"]))          
     return HH_working_people
 

def HHH_relation_pos(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,HHH_relation_answer):
    HHH_relation_pos = np.nan
    for i in range(len(data[source][questionnaire][section][hh][ref_question_1]['Answer'])):
        if data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] == HHH_relation_answer:
            HHH_relation_pos = data[source][questionnaire][section][hh][ref_question_2]['Answer'][i]
            return HHH_relation_pos
        

def socio_status_HHH(data,source,questionnaire,section_1,section_2,hh,ref_question,HHH_relation_question,HHH_relation_answer):
    'ref_question is the re-categorized main occupation.'
    'HHH_relation_question is the name of the question which specifies the relation with the household head.'
    'HHH_relation_answer is the name of the answer which identifies the household head in HHH_relation_question.'
    
    socio_status_HHH = np.nan
    
    if questionnaire != 'Tanzania':
        if data[source][questionnaire][section_1][hh][HHH_relation_question]['Answer'].count(HHH_relation_answer)==1:
            pos_head = data[source][questionnaire][section_1][hh][HHH_relation_question]['Answer'].index(HHH_relation_answer)
            socio_status_HHH = data[source][questionnaire][section_2][hh][ref_question]['Answer'][pos_head]
        
    if questionnaire == 'Tanzania':
        for i in range(len(data[source][questionnaire][section_2][hh]['sdd_indid']['Answer'])):
            if data[source][questionnaire][section_2][hh]['sdd_indid']['Answer'][i] == data[source][questionnaire][section_1][hh]['HHH_relation_pos']['Answer']:
               socio_status_HHH = data[source][questionnaire][section_1][hh][HHH_relation_question]['Answer'][i]
               if socio_status_HHH == 'Employee' and isNaN(data[source][questionnaire][section_2][hh][ref_question]['Answer'][i]) == False:
                    if data[source][questionnaire][section_2][hh][ref_question]['Answer'][i] == 1:
                        socio_status_HHH = 'Employee farm'
                    else:
                        socio_status_HHH = 'Employee non-farm'
               elif socio_status_HHH == 'Employee' and isNaN(data[source][questionnaire][section_2][hh][ref_question]['Answer'][i]) == True:
                   socio_status_HHH = np.nan
    return socio_status_HHH
        
def HH_w_home_business(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3,ref_answer):
    HH_w_home_business = ['No',np.nan]
    if any(t == ref_answer for t in data[source][questionnaire][section][hh][ref_question_1]['Answer']):
        HH_w_home_business[0] = 'Yes'
        HH_w_home_business[1] = [idx for idx, element in enumerate(data[source][questionnaire][section][hh][ref_question_1]['Answer']) if element == ref_answer]
    else:
        for i in range(len(data[source][questionnaire][section][hh][ref_question_1]['Answer'])):
            if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer'][i]) == True and (data[source][questionnaire]['Derived_variables'][hh][ref_question_2]['Answer'][i] != 'Unemployed' and isNaN(data[source][questionnaire]['Derived_variables'][hh][ref_question_2]['Answer'][i]) == False):
                HH_w_home_business[0] = np.nan
                return HH_w_home_business
            elif isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer'][i]) == True and isNaN(data[source][questionnaire]['Derived_variables'][hh][ref_question_2]['Answer'][i]) == True and data[source][questionnaire][section][hh][ref_question_3]['Answer'][i] >= 15:
                HH_w_home_business[0] = np.nan
                return HH_w_home_business
    return HH_w_home_business

def size_of_business(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,function_mode):
    'Function_mode is roster if multiple respondent or single_respondent if only one member answered'
    if function_mode == 'roster':
        size_of_business = [np.nan,np.nan]
        if isNaN(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == False:
            if len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])==1:
                pos_business = data[source][questionnaire][section_1][hh][ref_question_1]['Answer']
                size_of_business[0] = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][pos_business[0]]
                size_of_business[1] = pos_business
            elif len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])>1:
                pos_business = data[source][questionnaire][section_1][hh][ref_question_1]['Answer']
                temp = []
                for i in pos_business:
                    temp += [data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][i]]
                size_of_business[0] = max(temp)
                size_of_business[1] = [idx for idx, element in enumerate(data[source][questionnaire][section_2][hh][ref_question_2]['Answer']) if element == max(temp)]
                if len(size_of_business[1])!=1:
                    size_of_business = [np.nan,np.nan]
    elif function_mode == 'single_respondent':
        size_of_business = np.nan
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Yes':
            size_of_business = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0]                
    return size_of_business

def seasonal_business(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,function_mode):
    'Function_mode is roster if multiple respondent or single_respondent if only one member answered'
    seasonal_business = np.nan
    if function_mode == 'roster':
        if isNaN(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == False:        
            if data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0]] == 12:
                seasonal_business = 'No'
            elif isNaN(data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0]]) == False:
                seasonal_business = 'Yes'
    elif function_mode == 'single_respondent':
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Yes' or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Business':
            if data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0] == 0 or data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0] == 'Yes':
                seasonal_business = 'Yes'
            elif data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0] == 1 or data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0] == 'No':
                seasonal_business = 'No'        
    elif function_mode == 'LSMS':
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Non-agri':
            if data[source][questionnaire][section_2][hh][ref_question_2]['Answer'] == 12:
                seasonal_business = 'No'
            else:
                seasonal_business = 'Yes'
    return seasonal_business
    
def type_of_business(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_answer,function_mode):
    'Function_mode is roster if multiple respondent or single_respondent if only one member answered'
    type_of_business = [np.nan, np.nan]
    if function_mode == 'roster':
        check = []
        pos_business = [idx for idx, element in enumerate(data[source][questionnaire][section_2][hh][ref_question_2]['Answer']) if element in BUSINESS]
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) if element == ref_answer]
        pos_removed = set(pos_business) - set(pos_yes)
        pos = set(pos_business) - set(pos_removed)
        pos = list(pos)
        if len(pos)>0:
            if ((data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][pos[0]] != 555) and (math.isnan(data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][pos[0]])== False)):
                same = data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][pos[0]]
                for i in pos:
                    if ((data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][i] != 555) and (math.isnan(data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][i])== False)):
                        check.append(same == data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][i])
                if all(check) is True:
                    type_of_business[0] = data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][i]
                    type_of_business[1] = pos
    if function_mode == 'LSMS':
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Agri':
            type_of_business[0] = 'A'
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Non-agri':
            type_of_business[0] = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][data[source][questionnaire][section_1][hh][ref_question_3]['Answer']]
    return type_of_business

def HH_w_home_business_LSMS(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3):
    HH_w_home_business_LSMS = ['No',np.nan]
    temp1 = 0
    temp2 = 0
    for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == 1:
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == 1 or data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == 2:
                temp1 += 1
            elif isNaN(data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i]):
                temp2 += 1
    if temp1 > 0:
        HH_w_home_business_LSMS[0] = 'Yes'
        HH_w_home_business_LSMS[1] = 'Agri'
    elif temp1 == 0 and temp2 > 0:
        HH_w_home_business_LSMS[0] = np.nan
    if any(t == 1 for t in data[source][questionnaire][section_2][hh][ref_question_3]['Answer']):
        if HH_w_home_business_LSMS[0] == 'Yes':
            HH_w_home_business_LSMS[1] = 'Multiple'
        elif HH_w_home_business_LSMS[0] == 'No' or isNaN(HH_w_home_business_LSMS[0]):
            HH_w_home_business_LSMS[0] = 'Yes'
            HH_w_home_business_LSMS[1] = 'Non-agri'
    return HH_w_home_business_LSMS

def size_of_business_LSMS(data,source,questionnaire,hh):
    size_of_business_LSMS = [np.nan,np.nan,np.nan]
    overall_agri = 0
    overall_non_agri = 0
    if data[source][questionnaire]['Derived_variables'][hh]['HH_with_home_business_class']['Answer'] == 'Agri' or data[source][questionnaire]['Derived_variables'][hh]['HH_with_home_business_class']['Answer'] == 'Multiple':
        food_crops = []
        try: food_crops.append(sum(t for t in data[source][questionnaire]['ag_sec_5a'][hh]['ag5a_03']['Answer'] if isNaN(t) == False))
        except: aaa = 1
        try: food_crops.append(sum(t for t in data[source][questionnaire]['ag_sec_5b'][hh]['ag5b_03']['Answer'] if isNaN(t) == False))
        except: aaa = 1
        try: food_crops = statistics.mean(food_crops)
        except: food_crops = 0
        
        crops_residue = []
        try: crops_residue.append(sum(t for t in data[source][questionnaire]['ag_sec_5a'][hh]['ag5a_35']['Answer'] if isNaN(t) == False))
        except: aaa = 1
        try: crops_residue.append(sum(t for t in data[source][questionnaire]['ag_sec_5b'][hh]['ag5b_35']['Answer'] if isNaN(t) == False))
        except: aaa = 1
        try: crops_residue = statistics.mean(crops_residue)
        except: crops_residue = 0
        
        try: fruits = sum(t for t in data[source][questionnaire]['ag_sec_7a'][hh]['ag7a_04']['Answer'] if isNaN(t) == False)
        except: fruits = 0
        try: permanent_crops = sum(t for t in data[source][questionnaire]['ag_sec_7b'][hh]['ag7b_04']['Answer'] if isNaN(t) == False)
        except: permanent_crops = 0
        try: byproducts = sum(t for t in data[source][questionnaire]['ag_sec_10'][hh]['ag10_11']['Answer'] if isNaN(t) == False)
        except: byproducts = 0
        
        overall_agri = sum([food_crops,crops_residue,fruits,permanent_crops,byproducts])/12
    if data[source][questionnaire]['Derived_variables'][hh]['HH_with_home_business_class']['Answer'] == 'Non-agri' or data[source][questionnaire]['Derived_variables'][hh]['HH_with_home_business_class']['Answer'] == 'Multiple':
        if any(isNaN(t) == True for t in data[source][questionnaire]['hh_sec_n'][hh]['hh_n13_2']['Answer']):
            return size_of_business_LSMS
        else:
            monthly_all_business = []
            for i in range(len(data[source][questionnaire]['hh_sec_n'][hh]['hh_n13_2']['Answer'])):
                if data[source][questionnaire]['hh_sec_n'][hh]['hh_n13_1']['Answer'][i] == 1:
                    monthly_all_business.append(data[source][questionnaire]['hh_sec_n'][hh]['hh_n13_2']['Answer'][i]*4)
                else: monthly_all_business.append(data[source][questionnaire]['hh_sec_n'][hh]['hh_n13_2']['Answer'][i])
            overall_non_agri = max(monthly_all_business)
            pos_business_non_agri = [idx for idx, element in enumerate(monthly_all_business) if element == max(monthly_all_business)]
            if len(pos_business_non_agri)!=1:
                return size_of_business_LSMS
    if overall_agri > overall_non_agri:
        size_of_business_LSMS[0] = overall_agri
        size_of_business_LSMS[1] = 'Agri'
    elif overall_agri < overall_non_agri:
        size_of_business_LSMS[0] = overall_non_agri
        size_of_business_LSMS[1] = 'Non-agri'
        size_of_business_LSMS[2] = pos_business_non_agri[0]
    return size_of_business_LSMS

def size_of_business_employees_LSMS(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,clusters):
    size_of_business_employees_LSMS = np.nan
    temp = 0
    if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Non-agri':
        for i in clusters['Employees_cluster']:
            if isNaN(data[source][questionnaire][section_2][hh][i]['Answer'][data[source][questionnaire][section_1][hh][ref_question_2]['Answer']]) == False:
                temp += 1
        temp += data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][data[source][questionnaire][section_1][hh][ref_question_2]['Answer']]
        size_of_business_employees_LSMS = temp
    return size_of_business_employees_LSMS

def age_of_business_LSMS(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3):
    age_of_business_LSMS = np.nan
    if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == 'Non-agri':
        if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][data[source][questionnaire][section_1][hh][ref_question_2]['Answer']] == 2014:
            age_of_business_LSMS = data[source][questionnaire]['Derived_variables'][hh]['Survey_date']['Answer']-data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][data[source][questionnaire][section_1][hh][ref_question_2]['Answer']]
        else:
            age_of_business_LSMS = data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][data[source][questionnaire][section_1][hh][ref_question_2]['Answer']]
    return age_of_business_LSMS

def filtering(data,source,questionnaire,section,hh,ref_question,wrong_answer_1,wrong_answer_2):
    filtering = data[source][questionnaire][section][hh][ref_question]['Answer'][0]
    if (data[source][questionnaire][section][hh][ref_question]['Answer'][0] == wrong_answer_1) or (data[source][questionnaire][section][hh][ref_question]['Answer'][0] == wrong_answer_2):
        filtering= np.nan
    
    return filtering

def filtering_derived(data,source,questionnaire,section,hh,ref_question,wrong_answer_1,wrong_answer_2):
    filtering = data[source][questionnaire][section][hh][ref_question]['Answer']
    if (data[source][questionnaire][section][hh][ref_question]['Answer'] == wrong_answer_1) or (data[source][questionnaire][section][hh][ref_question]['Answer'] == wrong_answer_2):
        filtering= np.nan
    
    return filtering

# dwelling_ownership(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'b_b_7','b_b_8','Yes','No','Rented','Free')
def dwelling_ownership(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_yes,ref_no,ref_rented,ref_free):
    dwelling_ownership = np.nan
    if data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] == ref_yes:
        dwelling_ownership = 'Owned'
    elif (data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] == ref_no) and (data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] == ref_rented):
        dwelling_ownership = 'Rented'
    elif (data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] == ref_no) and (data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] == ref_free):
        dwelling_ownership = 'Used for free'
        
    return dwelling_ownership

# dwelling_toilet(data,source,questionnaire,'Derived_variables',hh,'Dwelling_toilet_1','Dwelling_toilet_2','Dwelling_toilet_3','Dwelling_toilet_3','not_list')
def dwelling_toilet(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3,ref_question_4,function_mode):
    'Function_mode depends if the answer is coming from a list or not'
    if function_mode == 'not_list':
        if ((data[source][questionnaire][section][hh][ref_question_1]['Answer'] == 1) or (data[source][questionnaire][section][hh][ref_question_2]['Answer'] == 1) or (data[source][questionnaire][section][hh][ref_question_3]['Answer'] == 1) or (data[source][questionnaire][section][hh][ref_question_4]['Answer'] == 1)):
            dwelling_toilet= 1
        else:
            dwelling_toilet= 0
    elif function_mode == 'list':
        if ((data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] == 1) or (data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] == 1) or (data[source][questionnaire][section][hh][ref_question_3]['Answer'][0] == 1) or (data[source][questionnaire][section][hh][ref_question_4]['Answer'][0] == 1)):
            dwelling_toilet= 1
        else:
            dwelling_toilet= 0
    return dwelling_toilet

# dwelling_quality_index(data,source,questionnaire,'Derived_variables',hh,clusters)
def dwelling_quality_index(data,source,questionnaire,section,hh,clusters):
    dwelling_quality_index= 0
    temp = []
    for i in clusters['Dwelling_quality_cluster']:
        if any(t == i for t in data[source][questionnaire][section][hh].keys()):
            temp += [data[source][questionnaire][section][hh][i]['Answer']]
    if len(temp) == 5:
        dwelling_quality_index= sum(temp)/len(temp)
    else:
        dwelling_quality_index = np.nan
    return dwelling_quality_index
# access_credit(data,source,questionnaire,'MTF_HH_Core_Survey',hh,clusters,'string')
def access_credit(data,source,questionnaire,section,hh,clusters,type_of_answer):
    
    access_credit = np.nan
    j= 0
    temp = []
    while j <= len(clusters['Loan_cluster']):
        temp.append(False)
        j += 1
    if type_of_answer == 'string':
        for pos,i in enumerate(clusters['Loan_cluster']):
            if any(t == i for t in data[source][questionnaire][section][hh].keys()):
                if ((data[source][questionnaire][section][hh][i]['Answer'][0] != 'Cannot get a loan') and (isinstance(data[source][questionnaire][section][hh][i]['Answer'][0],str))):
                    temp[pos] = True
    if type_of_answer == 'integer':
        for pos,i in enumerate(clusters['Loan_cluster']):
             if any(t == i for t in data[source][questionnaire][section][hh].keys()):
                 if data[source][questionnaire][section][hh][i]['Answer'][0] == 1:
                     temp[pos] = True
    if type_of_answer == 'integer_Zambia':
        for pos,i in enumerate(clusters['Loan_cluster']):
            if any(t== i for t in data[source][questionnaire][section][hh].keys()):
                if isNaN(data[source][questionnaire][section][hh][i]['Answer'][0]) == False and data[source][questionnaire][section][hh][i]['Answer'][0] != 13:
                    temp[pos] = True
    if type_of_answer == 'boolean':
        i = clusters['Loan_cluster'][0]
        if ((data[source][questionnaire][section][hh][i]['Answer'][0] == 'Yes') or (data[source][questionnaire][section][hh][i]['Answer'][0] == 'yes')):
            access_credit = 'Yes'
        elif data[source][questionnaire][section][hh][i]['Answer'][0] == 'No':
            access_credit = 'No'
    if (type_of_answer == 'string' or type_of_answer == 'integer' or type_of_answer== 'integer_Zambia') and any(temp) == True:
        access_credit = 'Yes'
    else:
        access_credit = 'No'
    return access_credit

# price_alternative(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'f_f_candle_10','f_f_candle_11','f_f_3_Candle_1','Yes','candles','single_response')
def price_alternative(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3,ref_answer,function_mode,function_mode_2):
    price_alternative= np.nan
    if function_mode_2 == 'single_response':
        if function_mode == 'candles':
            if data[source][questionnaire][section][hh][ref_question_3] == ref_answer:
                if (data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] != 'Yes') and (data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] != 'Yes'):
                    Quantity = float(data[source][questionnaire][section][hh][ref_question_1]['Answer'][0])
                    Expenditure = float(data[source][questionnaire][section][hh][ref_question_2]['Answer'][0])
                    if (Quantity != 888 and Quantity != 0) and Expenditure != 888:
                            price_alternative = Expenditure/Quantity
        else: 
            if (data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] != 'Yes') and (data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] != 'Yes'):
                Quantity = float(data[source][questionnaire][section][hh][ref_question_1]['Answer'][0])
                Expenditure = float(data[source][questionnaire][section][hh][ref_question_2]['Answer'][0])
                if (Quantity != 888 and Quantity != 0) and Expenditure != 888:
                        price_alternative = Expenditure/Quantity
                        
    if function_mode_2 == 'roster':
            Quantity = float(data[source][questionnaire][section][hh][ref_question_1]['Answer'][ref_answer])
            Expenditure = float(data[source][questionnaire][section][hh][ref_question_2]['Answer'][ref_answer])
            if (Quantity != 888) and (Quantity != 0):
                if (Expenditure != 888):
                    price_alternative = Expenditure/Quantity
                    
    if function_mode_2 == 'roster_Zambia':
        for pos,i in enumerate(data[source][questionnaire][section][hh][ref_question_1]['Answer']):
           if i == ref_answer:
               Expenditure = float(data[source][questionnaire][section][hh][ref_question_2]['Answer'][pos])
               Quantity = float(data[source][questionnaire][section][hh][ref_question_3]['Answer'][pos])
               if (Quantity != -8) and (Quantity != 0):
                 if (Expenditure != -8):  
                     price_alternative = Expenditure/Quantity
    return price_alternative

# expenditure(data,source,questionnaire,'MTF_HH_Core_Survey','-','-',hh,clusters,1,1,1,'single_response')
def expenditure(data,source,questionnaire,section_1,section_2,section_3,hh,clusters,weekly,monthly,yearly,function_mode):
    expenditure = 0
    if function_mode == 'single_response':
        if weekly == 1:
            for i in clusters['Weekly_expenditure_cluster']:
                if data[source][questionnaire][section_1][hh][i]['Answer'][0] == 'Do not know' or data[source][questionnaire][section_1][hh][i]['Answer'][0] == '111' or math.isnan(float(data[source][questionnaire][section_1][hh][i]['Answer'][0])) == True:
                    expenditure= np.nan
                    return expenditure
                expenditure += float(data[source][questionnaire][section_1][hh][i]['Answer'][0])*52
        if monthly == 1:
            for i in clusters['Monthly_expenditure_cluster']:
                if data[source][questionnaire][section_1][hh][i]['Answer'][0] == 'Do not know':
                    expenditure= np.nan
                    return expenditure
                if i == 'l_l_17' and math.isnan(float(data[source][questionnaire][section_1][hh][i]['Answer'][0]))== True:
                    data[source][questionnaire][section_1][hh][i]['Answer'][0]= 0
                if data[source][questionnaire][section_1][hh][i]['Answer'][0] == '111' or math.isnan(float(data[source][questionnaire][section_1][hh][i]['Answer'][0])) == True:
                    expenditure= np.nan
                    return expenditure
                expenditure += float(data[source][questionnaire][section_1][hh][i]['Answer'][0])*12
        if yearly == 1:
            for i in clusters['Yearly_expenditure_cluster']:
                if data[source][questionnaire][section_1][hh][i]['Answer'][0] == 'Do not know' or data[source][questionnaire][section_1][hh][i]['Answer'][0] == '111' or math.isnan(float(data[source][questionnaire][section_1][hh][i]['Answer'][0])) == True:
                    expenditure= np.nan
                    return expenditure
                expenditure += float(data[source][questionnaire][section_1][hh][i]['Answer'][0])
        expenditure= expenditure/12
    
    if function_mode == 'roster':
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_1][hh]['L_1_13']['Answer']) if element == 1]
        for i in pos_yes:
            if  data[source][questionnaire][section_1][hh]['L_consumption_purchased']['Answer'][i] == 888:
                expenditure = np.nan
                return expenditure
            expenditure += data[source][questionnaire][section_1][hh]['L_consumption_purchased']['Answer'][i]*52
        
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_2][hh]['L_14_22']['Answer']) if element == 1]
        for i in pos_yes:
            if data[source][questionnaire][section_2][hh]['L_expenditure']['Answer'][i] == 888:
                expenditure = np.nan
                return expenditure
            expenditure += data[source][questionnaire][section_2][hh]['L_expenditure']['Answer'][i]*12
        
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_3][hh]['L_23_36']['Answer']) if element == 1]
        for i in pos_yes:
            if data[source][questionnaire][section_3][hh]['L_expenditure_12months']['Answer'][i] == 888:
                expenditure = np.nan
                return expenditure
            expenditure += data[source][questionnaire][section_3][hh]['L_expenditure_12months']['Answer'][i]
        expenditure = expenditure/12
    
    if function_mode == 'roster_Zambia':
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_1][hh]['litem']['Answer']) if element in [1,2,3,4,5,6,7,8,9,10,11,12,13]]
        for i in pos_yes:
            if data[source][questionnaire][section_1][hh]['L2A']['Answer'][i] != -8:
                expenditure += data[source][questionnaire][section_1][hh]['L2A']['Answer'][i]*52
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_1][hh]['litem']['Answer']) if element in [14,15,16,17,18,19,20,21,22]]
        for i in pos_yes:
            if data[source][questionnaire][section_1][hh]['L2A']['Answer'][i] != -8:
                expenditure += data[source][questionnaire][section_1][hh]['L2A']['Answer'][i]*12
        pos_yes = [idx for idx, element in enumerate(data[source][questionnaire][section_1][hh]['litem']['Answer']) if element in [23,24,25,26,27,28,29,30,31,32,33,34,35]]
        for i in pos_yes:
            if data[source][questionnaire][section_1][hh]['L2A']['Answer'][i] != -8:
                expenditure += data[source][questionnaire][section_1][hh]['L2A']['Answer'][i]
        expenditure= expenditure/12
    return expenditure
    
    
    if function_mode == 'multi_section':
        total = 0
        for section in ['hh_sec_c','hh_sec_d','hh_sec_f','hh_sec_i','hh_sec_j1','hh_sec_k','hh_sec_l']:
            for question in clusters['Expenditure_yearly_cluster']:
                try:
                    for i in range(len(data[source][questionnaire][section][hh][question]['Answer'])):
                        if isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == False:
                            temp = data[source][questionnaire][section][hh][question]['Answer'][i]/12
                            total += temp
                except: 
                    total = total
            for question in clusters['Expenditure_monthly_cluster']:
                try:
                    for i in range(len(data[source][questionnaire][section][hh][question]['Answer'])):
                        if isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == False:
                            temp = data[source][questionnaire][section][hh][question]['Answer'][i]
                            total += temp
                        elif section == 'hh_sec_d' and isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == True:
                            expenditure = np.nan
                            return expenditure
                except:
                    total = total
            for question in clusters['Expenditure_weekly_cluster']:
                try:
                    for i in range(len(data[source][questionnaire][section][hh][question]['Answer'])):
                        if isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == False:
                            temp = data[source][questionnaire][section][hh][question]['Answer'][i]*4
                            total += temp
                        elif question == 'hh_f03' and data[source][questionnaire][section][hh]['hh_f02']['Answer'][i] == 1:
                            expenditure = np.nan
                            return expenditure
                except:
                    total = total
        for section in ['hh_sec_k']:
            for question in clusters['Expenditure_multi_period_cluster']:
                for i in range(len(data[source][questionnaire][section][hh][question]['Answer'])):
                    if i in [0,1,2]:
                        if isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == False:
                            temp = data[source][questionnaire][section][hh][question]['Answer'][i]*4
                            total += temp
                    else:
                        if isNaN(data[source][questionnaire][section][hh][question]['Answer'][i]) == False:
                            temp = data[source][questionnaire][section][hh][question]['Answer'][i]
                            total += temp
        expenditure = total
    return expenditure
    

def asset(data,source,questionnaire,section_1,section_2,hh,ref_question,function_mode):
    asset = 'No'
    if function_mode == 'kenya':
        if any(t == 1 for t in data[source][questionnaire][section_2][hh][ref_question]['Answer']):
            asset = 'Yes'
    if function_mode == 'nigeria':
        for i in range(len(data[source][questionnaire][section_1][hh]['asset_list']['Answer'])):
           if data[source][questionnaire][section_1][hh]['own_asset']['Answer'][i] == 1 and data[source][questionnaire][section_2][hh][ref_question]['Answer'][i] == 1:
              asset = 'Yes'
    if function_mode == 'zambia':
        for i in range(len(data[source][questionnaire][section_1][hh]['mitem']['Answer'])):
              if data[source][questionnaire][section_1][hh]['M1B']['Answer'][i] == 1 and data[source][questionnaire][section_2][hh][ref_question]['Answer'][i] == 1:
                 asset = 'Yes'
    if function_mode == 'tanzania_vehicle':
        if data[source][questionnaire][section_1][hh]['hh_m01']['Answer'][24] > 0 or data[source][questionnaire][section_1][hh]['hh_m01']['Answer'][25] > 0:
          asset == 'Yes'
    if function_mode == 'tanzania_livestock_small':
        if data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][6] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][7] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][8] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][12] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][13] == 1:
            asset = 'Yes'
    if function_mode == 'tanzania_livestock_large':
        if data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][0] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][1] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][2] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][3] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][4] == 1 or data[source][questionnaire][section_1][hh]['lf02_01']['Answer'][5] == 1:
            asset = 'Yes'
    return asset

# connection_type(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'c_c_2','c_c_38','c_c_q122_3','Yes','Yes',1)
def connection_type(data,source,questionnaire,section_1,hh,ref_question_1,ref_question_2,ref_question_3,ref_answer_grid,ref_answer_minigrid,ref_answer_SHS):
    connection_type = np.nan
    if section_1 == 'Derived_variables':
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == ref_answer_grid:
            connection_type = 'National grid'
        elif data[source][questionnaire][section_1][hh][ref_question_2]['Answer'] == ref_answer_minigrid:
            connection_type = 'Local mini-grid'
        elif data[source][questionnaire][section_1][hh][ref_question_3]['Answer'] == ref_answer_SHS:
            connection_type = 'Solar Home System'
    else:    
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == ref_answer_grid:
            connection_type = 'National grid'
        elif data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0] == ref_answer_minigrid:
            connection_type = 'Local mini-grid'
        elif data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][0] == ref_answer_SHS:
            connection_type = 'Solar Home System'
    return connection_type

# measurement_age(data,source,questionnaire,'MTF_HH_Core_Survey','Derived_variables',hh,'c_c_7','c_c_38','MTF_HH_Solar_Roster','c_135_yrs','c_127_device')
def measurement_age(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,section_solar,ref_question_solar_1,ref_question_solar_2):
    measurement_age = np.nan
    try:
        if data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'National grid':
            if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] != 'HH has always had grid connection' and data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] != "Don't know":
                measurement_age = float(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0])
        if data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'Local mini-grid':
            measurement_age = float(data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0])
        if data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'Solar Home System':
            temp = []
            for i in range(len(data[source][questionnaire][section_solar][ref_question_solar_1]['Answer'])):
                if data[source][questionnaire][section_solar][ref_question_solar_2]['Answer'][i] == 3 or data[source][questionnaire][section_solar][ref_question_solar_2]['Answer'][i] == 'Solar home system (Solar PV system)':
                    temp.append(data[source][questionnaire][section_solar][hh][ref_question_solar_1]['Answer'][i])
            if len(temp) > 0:
                measurement_age= max(temp)        
        return measurement_age   
    except:
        return measurement_age

# hours_available_electricity(data,source,questionnaire,'mtf_ng_hh_sec_c','Derived_variables',hh,'C_28b','C68b','C169b','mtf_ng_hh_sec_c_solar','C146',3)
def hours_available_electricity(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,section_solar_devices,main_device_question,valid_answer):
    hours_available_electricity = np.nan

    try:
        if data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'National grid':
            hours_available_electricity = float(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0])
        elif data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'Local mini-grid':
            hours_available_electricity = float(data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0])
        elif data[source][questionnaire][section_2][hh]['Connection_type']['Answer'] == 'Solar Home System':
            main_shs_dev = main_shs_device(data,source,questionnaire,hh,section_solar_devices,main_device_question)
            if main_shs_dev == valid_answer:
                hours_available_electricity = float(data[source][questionnaire][section_1][hh][ref_question_3]['Answer'][0])
        return hours_available_electricity
    except:
        return hours_available_electricity                                    
    'Questa è in Core Survey per SHS, ma ha bisogno che il primo device di Solar Roster sia SHS'
    'Per la Nigeria bisogna capire come capire se il MSD è SHS o meno'

def main_shs_device(data,source,questionnaire,hh,section_solar_devices,main_device_question):
    main_shs_dev = data[source][questionnaire][section_solar_devices][hh][main_device_question]['Answer'][0]
    return main_shs_dev

# electricity_expenditure(data,source,questionnaire,'Derived_variables','MTF_HH_Core_Survey',hh,'c_c_20','c_c_20','monthly')
def electricity_expenditure(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,function_mode):
    electricity_expenditure = np.nan
    if function_mode == 'monthly':
        if data[source][questionnaire][section_1][hh]['Connection_type']['Answer']== 'National grid':
            electricity_expenditure = float(data[source][questionnaire][section_2][hh][ref_question_1]['Answer'][0])
        elif data[source][questionnaire][section_1][hh]['Connection_type']['Answer'] == 'Local mini-grid':
            electricity_expenditure = float(data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0])
    elif function_mode == 'not monthly':
        if type(data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]) == float or type(data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]) == int:
            if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'D2':
                electricity_expenditure =  data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]*15
            elif data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'W':
                electricity_expenditure =  data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]*4
            elif data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'W2' or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'M/2':
                electricity_expenditure =  data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]*2
            elif data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'M':
                electricity_expenditure =  data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]
            elif data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][0] == 'M3':
                electricity_expenditure =  data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]/3
    return electricity_expenditure
# land_owned(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'n_n_1b','n_n_1b_unit','Acre','sq metres','-','-','-')
def land_owned(data,source,questionnaire,section,hh,question_dimension,question_unit,ref_answer_unit_acre,ref_answer_unit_sqm,ref_answer_unit_hectare,ref_answer_unit_plot,ref_answer_unit_ridg):
    land_owned = np.nan
    if data[source][questionnaire][section][hh][question_unit]['Answer'][0] == ref_answer_unit_acre:
        land_owned = float(data[source][questionnaire][section][hh][question_dimension]['Answer'][0])*4046.86
    elif data[source][questionnaire][section][hh][question_unit]['Answer'][0] == ref_answer_unit_sqm:
        land_owned = float(data[source][questionnaire][section][hh][question_dimension]['Answer'][0])
    elif data[source][questionnaire][section][hh][question_unit]['Answer'][0] == ref_answer_unit_hectare:
        land_owned = float(data[source][questionnaire][section][hh][question_dimension]['Answer'][0])*10000
    elif data[source][questionnaire][section][hh][question_unit]['Answer'][0] == ref_answer_unit_plot:
        land_owned = float(data[source][questionnaire][section][hh][question_dimension]['Answer'][0])*900
    elif data[source][questionnaire][section][hh][question_unit]['Answer'][0] == ref_answer_unit_ridg:
        land_owned = float(data[source][questionnaire][section][hh][question_dimension]['Answer'][0])*38.1
    return land_owned

def land_multiple_owned(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3):
    land_multiple_owned = 0
    for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
        if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == 1 or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == 2 or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == 5:
            if isNaN(data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][i]) == False:
                land_multiple_owned  += data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][i]*4046.86
            else:
                if isNaN(data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][i]) == False:
                    land_multiple_owned += data[source][questionnaire][section_2][hh][ref_question_3]['Answer'][i]*4046.86
                else:
                    land_multiple_owned = np.nan
                    return land_multiple_owned
        else:
            land_multiple_owned = np.nan
    return land_multiple_owned

# electricity_consumption(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'c_c_21',888,111,'National grid')
def electricity_consumption(data,source,questionnaire,section,hh,ref_question,wrong_answer_1,wrong_answer_2,function_mode):
    electricity_consumption = np.nan
    if data[source][questionnaire]['Derived_variables'][hh]['Connection_type']['Answer'] == function_mode:
        electricity_consumption = filtering(data,source,questionnaire,section,hh,ref_question,wrong_answer_1,wrong_answer_2)
    return electricity_consumption

def electricity_tariff(data,source,questionnaire,section,hh,ref_question_1,ref_question_2):
    electricity_tariff = np.nan
    if data[source][questionnaire][section][hh][ref_question_2]['Answer'] != 0:
        electricity_tariff = data[source][questionnaire][section][hh][ref_question_1]['Answer']/data[source][questionnaire][section][hh][ref_question_2]['Answer']
    return electricity_tariff
# tariff_type(data,source,questionnaire,'MTF_HH_Core_Survey',hh,'c_c_12','No one','c_c_17',map_cat,clusters)
def tariff_type(data,source,questionnaire,section,hh,ref_question,ref_answer,ref_question_1,map_cat,clusters):
    tariff_type = np.nan
    tariff_type_list = []
    if data[source][questionnaire][section][hh][ref_question]['Answer'][0] == ref_answer:
        tariff_type = 'No bill'
        return tariff_type
    tariff_type_list = re_categorization(data,source,questionnaire,section,hh,ref_question_1,'','',map_cat,'Tariff_type',clusters)
    tariff_type = tariff_type_list[0]

    return tariff_type

def pre_paid_tariff(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_answer_1,ref_answer_2):
    pre_paid_tariff = np.nan
    if data[source][questionnaire]['Derived_variables'][hh]['Tariff_type']['Answer'] == 'Consumption based':
        if data[source][questionnaire][section][hh][ref_question_1]['Answer'][0] == ref_answer_1:
            if data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] == ref_answer_1:
                  pre_paid_tariff = 'Yes'
            elif data[source][questionnaire][section][hh][ref_question_2]['Answer'][0] == ref_answer_2:
                pre_paid_tariff = 'No'

    return pre_paid_tariff

# presence_appliances(data,source,questionnaire,'mtf_ng_hh_sec_n_elec_asset',hh,'own_asset','item_id',25,'long')
def presence_appliances(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_appliance,function_mode):
    'function_mode can take values of "string" when it is present a string with the codes of the appliances present...'
    ' "long"" when two columns must be acquired, one with the item-id and one with a boolean variable indicating presence...'
    ' or "presence", when the only appliances reported are the ones that are present'
    presence_appliances= np.nan
    if function_mode == 'string':
        if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer'][0]) == False: 
            temp= data[source][questionnaire][section][hh][ref_question_1]['Answer'][0].split()
            presence_appliances= 0
            if any(t == ref_appliance for t in temp):
                presence_appliances = 1
    if function_mode == 'long':
        for i in range(len(data[source][questionnaire][section][hh][ref_question_1]['Answer'])):
            if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer'][i]) == False:
                presence_appliances = 0
                if data[source][questionnaire][section][hh][ref_question_2]['Answer'][i] == ref_appliance and data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] >= 1:
                    presence_appliances = 1
                    return presence_appliances
    if function_mode == 'presence':
        for i in range(len(data[source][questionnaire][section][hh][ref_question_1]['Answer'])):
            presence_appliances = 0
            if data[source][questionnaire][section][hh][ref_question_1]['Answer'][i] == ref_appliance:
                presence_appliances = 1
                return presence_appliances
    return presence_appliances

def number_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):   
    number_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance:
                number_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        number_appliances = 0
    return number_appliances

def average_daily_usage_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):
    average_daily_usage_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance and data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] < 1440:
                average_daily_usage_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        average_daily_usage_appliances = 0
    return average_daily_usage_appliances

def nominal_power_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):
    nominal_power_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance:
                nominal_power_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        nominal_power_appliances = 0
    return nominal_power_appliances
    
def frequency_of_use_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):
    frequency_of_use_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance and isNaN(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]) == False:
                frequency_of_use_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] / 7
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        frequency_of_use_appliances = 0
    return frequency_of_use_appliances

def window_time_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):
    window_time_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance:
                window_time_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        window_time_appliances = 0
    return window_time_appliances

def minimum_time_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance):
    minimum_time_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance and data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] < 1440:
                minimum_time_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    elif data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 0:
        minimum_time_appliances = 0
    return minimum_time_appliances
# multi_unification_appliances(data,source,questionnaire,'Derived_variables',hh,'Presence_radio','Presence_stereo',888,888,'presence')
def multi_unification_appliances(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3,ref_question_4,function_mode):
    multi_unification_appliances = np.nan
    if function_mode == 'presence':
        if is888(data,source,questionnaire,section,hh,ref_question_1) == 1 or is888(data,source,questionnaire,section,hh,ref_question_2) == 1 or is888(data,source,questionnaire,section,hh,ref_question_3) == 1 or is888(data,source,questionnaire,section,hh,ref_question_4) == 1:
            multi_unification_appliances = 1
        else: 
            ref_questions_list = [ref_question_1,ref_question_2,ref_question_3,ref_question_4]
            count_NaN = 0
            count_valid= 0
            for i in ref_questions_list:
                if isNaN(is888(data,source,questionnaire,section,hh,i)) == True:
                    count_NaN += 1
                if is888(data,source,questionnaire,section,hh,i) != 888:
                    count_valid += 1
            if count_NaN != count_valid:
                multi_unification_appliances = 0
    if function_mode == 'number':
        ref_questions_list = [ref_question_1,ref_question_2,ref_question_3,ref_question_4]
        answers_list = []
        for i in ref_questions_list:
            if is888(data,source,questionnaire,section,hh,i) != 888:
                answers_list.append(is888(data,source,questionnaire,section,hh,i))
        multi_unification_appliances = sum(answers_list)
    return multi_unification_appliances

def user_unification(data,source,questionnaire,section,hh,ref_question_1,ref_question_2,ref_question_3, function_mode):
    if function_mode == 'different_sections':
        'The variable is not nan-ized at the beginning of the function because, in this mode, an answer should always be present if no mistakes happen'
        try: user_unification = data[source][questionnaire][section][hh][ref_question_1]['Answer']
        except:
            try: user_unification = data[source][questionnaire][section][hh][ref_question_2]['Answer']
            except:
                try: user_unification = data[source][questionnaire][section][hh][ref_question_3]['Answer']
                except: print('Error')
    if function_mode == 'same_section':
        'NB: only one (or none) of the answers should be not nan for the fuction to work properly'
        user_unification = np.nan
        temp = 0
        try:
            if isNaN(data[source][questionnaire][section][hh][ref_question_1]['Answer']) == False:
                user_unification = data[source][questionnaire][section][hh][ref_question_1]['Answer'] 
        except: temp +=1
        try:
            if isNaN(data[source][questionnaire][section][hh][ref_question_2]['Answer']) == False:
                user_unification = data[source][questionnaire][section][hh][ref_question_2]['Answer']
        except: temp +=1
        try:
            if isNaN(data[source][questionnaire][section][hh][ref_question_3]['Answer']) == False:
                user_unification = data[source][questionnaire][section][hh][ref_question_3]['Answer']
        except: temp +=1
    return user_unification

# years_of_HHH_in_community(data,source,questionnaire,'MTF_HH_Core_Survey','MTF_HH_Roster',hh,'a_4_rel_hhh','b_b_4','b_b_1','Head','multi_section')
def years_of_HHH_in_community(data,source,questionnaire,section_1,section_2,hh,HHH_relation_question,ref_question_1,ref_question_2,HHH_relation_answer,function_mode):
    years_of_HHH_in_community = np.nan
    
    if function_mode == 'roster':
        if data[source][questionnaire][section_1][hh][HHH_relation_question]['Answer'].count(HHH_relation_answer)==1:
            pos_head = data[source][questionnaire][section_1][hh][HHH_relation_question]['Answer'].index(HHH_relation_answer)
            if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][pos_head] != 99:
                years_of_HHH_in_community = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][pos_head]
            else:
                years_of_HHH_in_community = data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][pos_head]
    if function_mode == 'multi_section':
        pos_head = data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][0]
        try:
            if data[source][questionnaire][section_2][hh][HHH_relation_question]['Answer'][pos_head - 1] == HHH_relation_answer:
                years_of_HHH_in_community = filtering(data,source,questionnaire,section_1,hh,ref_question_1,888,111)
        except:
            return years_of_HHH_in_community
    return years_of_HHH_in_community

def timenum_purchase_appliances(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_question_2,ref_question_3,ref_appliance,position):
    timenum_purchase_appliances = np.nan
    if data[source][questionnaire][section_2][hh][ref_question_3]['Answer'] == 1:
        for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
            if data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][i] == ref_appliance:
                if type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]) == str:
                    try:
                        int(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i].split(" ")[position])
                        timenum_purchase_appliances = int(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i].split(" ")[position])
                    except: return timenum_purchase_appliances
                elif position == 0 and (type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]) == int or type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]) == float):
                    timenum_purchase_appliances = data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i]
    return timenum_purchase_appliances

def dwelling_age(data,source,questionnaire,section_1,hh,ref_question_1,ref_question_2):
    dwelling_age = np.nan
    if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][36] == 1:
        dwelling_age = data[source][questionnaire][section_1][hh][ref_question_2]['Answer'][36]
    return dwelling_age

def single_column_assignment(data,source,questionnaire,section,hh,ref_question,ref_answer,function_mode,positive_output,negative_ouput):
    single_column_assignment = np.nan
    if section == 'Derived_variables':
        temp = data[source][questionnaire][section][hh][ref_question]['Answer']
    else: temp = data[source][questionnaire][section][hh][ref_question]['Answer'][0]
    if function_mode == 'higher_than' and temp > ref_answer:
        single_column_assignment = positive_output
    if function_mode == 'equal_to' and temp == ref_answer:
        single_column_assignment = positive_output
    if function_mode == 'equal_to_else':
        if temp == ref_answer:
            single_column_assignment = positive_output
        else: single_column_assignment = negative_ouput
    if function_mode == 'not_empty':
        if isNaN(temp) == False:
            single_column_assignment = positive_output
    return single_column_assignment

def multisec_double_column_selection(data,source,questionnaire,section_1,section_2,hh,ref_question_1,ref_answer,ref_question_2,function_mode):
    multisec_double_column_selection = np.nan
    if function_mode == 'equal_to':
        if type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == str or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == int or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == float:
            if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == ref_answer:
                multisec_double_column_selection = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0]
        if type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == list:
            for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
                if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == ref_answer:
                    multisec_double_column_selection = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][i]
    if function_mode == 'equal_to_else_zero':
        if type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == str or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == int or data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == float:
            if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'] == ref_answer:
                multisec_double_column_selection = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][0]
            else: multisec_double_column_selection = 0
        if type(data[source][questionnaire][section_1][hh][ref_question_1]['Answer']) == list:
            for i in range(len(data[source][questionnaire][section_1][hh][ref_question_1]['Answer'])):
                if data[source][questionnaire][section_1][hh][ref_question_1]['Answer'][i] == ref_answer:
                    multisec_double_column_selection = data[source][questionnaire][section_2][hh][ref_question_2]['Answer'][i]
            if isNaN(multisec_double_column_selection) == True:
                multisec_double_column_selection = 0
    return multisec_double_column_selection