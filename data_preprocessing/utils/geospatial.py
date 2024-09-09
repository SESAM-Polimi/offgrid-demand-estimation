# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 16:03:36 2022

@author: Tommaso Ferrucci
"""
import numpy as np
import requests
import pandas as pd
from functions import isNaN

def GADM(data,source,questionnaire,section,hh,ref_question_lev_1,ref_question_lev_2,ref_question_lev_2_1,ref_question_lev_3):
    GADM = [np.nan, np.nan, np.nan, np.nan]
    if isNaN(data[source][questionnaire][section][hh][ref_question_lev_1]['Answer'][0]) == False:
        temp_1 = data[source][questionnaire][section][hh][ref_question_lev_1]['Answer'][0].lower()
        temp_1 = temp_1.replace('-',' ')
        temp_1 = temp_1.replace("'","")
        for i in list(data[source][questionnaire]['GADM_level_1'].keys()):
            "Possible extra check on opzional name"
            temp_GADM_1 = data[source][questionnaire]['GADM_level_1'][i]['NAME_1']['Answer'][0].lower()
            temp_GADM_1 = temp_GADM_1.replace('-',' ')
            temp_GADM_1 = temp_GADM_1.replace("'","")
            if temp_1 == temp_GADM_1:
                GADM[0] = data[source][questionnaire]['GADM_level_1'][i]['GID_1']['Answer'][0]
                GADM[1] = data[source][questionnaire]['GADM_level_1'][i]['NAME_1']['Answer'][0]
        if isNaN(GADM[1]) == False:
            temp_3 = np.nan
            temp_2 = np.nan
            temp_4 = np.nan
            if isNaN(data[source][questionnaire][section][hh][ref_question_lev_2]['Answer'][0]) == False:   
                temp_2 = data[source][questionnaire][section][hh][ref_question_lev_2]['Answer'][0].lower()
                temp_2 = temp_2.replace('-',' ')
                temp_2 = temp_2.replace("'","")
            if ref_question_lev_2_1 != '' and isNaN(data[source][questionnaire][section][hh][ref_question_lev_2_1]['Answer'][0]) == False:
                temp_3 = data[source][questionnaire][section][hh][ref_question_lev_1]['Answer'][0].lower() + ' ' + data[source][questionnaire][section][hh][ref_question_lev_2_1]['Answer'][0].lower()
                temp_3 = temp_3.replace('-',' ')
                temp_3 = temp_3.replace("'","")
                temp_4 = data[source][questionnaire][section][hh][ref_question_lev_2_1]['Answer'][0].lower()
                temp_4 = temp_4.replace('-',' ')
                temp_4 = temp_4.replace("'","")
            if isNaN(temp_2) == False or isNaN(temp_3) == False or isNaN(temp_4) == False:
                for i in list(data[source][questionnaire]['GADM_level_2'].keys()):
                    temp_GADM_1 = str(data[source][questionnaire]['GADM_level_2'][i]['NAME_1']['Answer'][0]).lower()
                    temp_GADM_1 = temp_GADM_1.replace('-',' ')
                    temp_GADM_1 = temp_GADM_1.replace("'","")
                    temp_GADM_2 = str(data[source][questionnaire]['GADM_level_2'][i]['NAME_2']['Answer'][0]).lower()
                    temp_GADM_2 = temp_GADM_2.replace('-',' ')
                    temp_GADM_2 = temp_GADM_2.replace("'","")
                    if temp_1 == temp_GADM_1 and (temp_2 == temp_GADM_2 or temp_3 == temp_GADM_2 or temp_4 == temp_GADM_2):
                        GADM[0] = data[source][questionnaire]['GADM_level_2'][i]['GID_2']['Answer'][0]
                        GADM[2] = data[source][questionnaire]['GADM_level_2'][i]['NAME_2']['Answer'][0]
                        return GADM
            if ref_question_lev_2_1 != '' and isNaN(data[source][questionnaire][section][hh][ref_question_lev_2_1]['Answer'][0]) == False and questionnaire == 'kenya':
                for i in list(data[source][questionnaire]['GADM_level_3'].keys()):
                    temp_GADM_3 = str(data[source][questionnaire]['GADM_level_3'][i]['NAME_3']['Answer'][0]).lower()
                    temp_GADM_3 = temp_GADM_3.replace('-',' ')
                    temp_GADM_3 = temp_GADM_3.replace("'","") 
                    temp_GADM_2 = str(data[source][questionnaire]['GADM_level_3'][i]['NAME_2']['Answer'][0]).lower()
                    temp_GADM_2 = temp_GADM_2.replace('-',' ')
                    temp_GADM_2 = temp_GADM_2.replace("'","")
                    if temp_4 == temp_GADM_3:
                        GADM[0] = data[source][questionnaire]['GADM_level_3'][i]['GID_2']['Answer'][0]
                        GADM[2] = data[source][questionnaire]['GADM_level_3'][i]['NAME_2']['Answer'][0]
                        return GADM
            if ref_question_lev_3 != '' and isNaN(data[source][questionnaire][section][hh][ref_question_lev_3]['Answer'][0]) == False and questionnaire == 'kenya':
                temp_5 = data[source][questionnaire][section][hh][ref_question_lev_3]['Answer'][0].lower()
                temp_5 = temp_5.replace('-',' ')
                temp_5 = temp_5.replace("'","")
                for i in list(data[source][questionnaire]['GADM_level_3'].keys()):
                    temp_GADM_3 = str(data[source][questionnaire]['GADM_level_3'][i]['NAME_3']['Answer'][0]).lower()
                    temp_GADM_3 = temp_GADM_3.replace('-',' ')
                    temp_GADM_3 = temp_GADM_3.replace("'","") 
                    temp_GADM_2 = str(data[source][questionnaire]['GADM_level_3'][i]['NAME_2']['Answer'][0]).lower()
                    temp_GADM_2 = temp_GADM_2.replace('-',' ')
                    temp_GADM_2 = temp_GADM_2.replace("'","")
                    if temp_5 == temp_GADM_3:
                        GADM[0] = data[source][questionnaire]['GADM_level_3'][i]['GID_2']['Answer'][0]
                        GADM[2] = data[source][questionnaire]['GADM_level_3'][i]['NAME_2']['Answer'][0]
                        return GADM
    return GADM

Village_variables = ['Climate1','City_dist','Grid_dist','Latitude','Longitude','masl','Population']
GADM_variables = ['Climate_majority','Population_mean','Relative_wealth_index','masl_mean']

# GIS_info(data,source,questionnaire,'Derived_variables',hh,'Latitude','','Village_level')
def GIS_info(data,source,questionnaire,section,hh,variable,ref_question,function_mode):
    "This is the section dedicated on Geospatial information"
    "1) Climate - climate zones are assigned based on the main climate present in the areas considered upon the highest level of GADM"
    GIS_info = np.nan
    ref_question_GADM = np.nan
    if function_mode == 'GADM_level':
        if variable in GADM_variables:
                if isNaN(data[source][questionnaire][section][hh][ref_question]['Answer']) == False:
                    if ref_question == 'GADM_level_1':
                        ref_question_GADM = 'NAME_1'
                    elif ref_question == 'GADM_level_2':
                        ref_question_GADM = 'NAME_2'
                    elif ref_question == 'GADM_level_3':
                        ref_question_GADM = 'NAME_3'
                    for i in list(data[source][questionnaire][ref_question].keys()):
                        temp = data[source][questionnaire][section][hh][ref_question]['Answer']
                        if ref_question == 'GADM_level_1':
                            if temp == data[source][questionnaire][ref_question][i][ref_question_GADM]['Answer'][0]:
                                GIS_info = data[source][questionnaire][ref_question][i][variable]['Answer'][0]
                                return GIS_info
                        elif ref_question == 'GADM_level_2':
                            if temp == data[source][questionnaire][ref_question][i][ref_question_GADM]['Answer'][0] and data[source][questionnaire][section][hh]['GADM_level_1']['Answer'] == data[source][questionnaire][ref_question][i]['NAME_1']['Answer'][0]:
                                GIS_info = data[source][questionnaire][ref_question][i][variable]['Answer'][0]
                                return GIS_info
                        elif ref_question == 'GADM_level_3':
                            if temp == data[source][questionnaire][ref_question][i][ref_question_GADM]['Answer'][0] and data[source][questionnaire][section][hh]['GADM_level_1']['Answer'] == data[source][questionnaire][ref_question][i]['NAME_1']['Answer'][0] and data[source][questionnaire][section][hh]['GADM_level_2']['Answer'] == data[source][questionnaire][ref_question][i]['NAME_2']['Answer'][0]:
                                GIS_info = data[source][questionnaire][ref_question][i][variable]['Answer'][0]
                                return GIS_info
                return GIS_info
    if function_mode == 'Village_level':
        if variable == 'GADM_level_1' or variable == 'GADM_level_2' or variable == 'GADM_level_3':
            if isNaN(data[source][questionnaire][section][hh]['Township/Village']['Answer']) == False:
                for i in list(data[source][questionnaire]['Village_GPS_info'].keys()):
                    temp = data[source][questionnaire][section][hh]['Township/Village']['Answer']
                    if temp == data[source][questionnaire]['Village_GPS_info'][i]['Name']['Answer'][0]:
                        GIS_info = data[source][questionnaire]['Village_GPS_info'][i][variable]['Answer'][0]
                        return GIS_info
        if variable in Village_variables:
            if isNaN(data[source][questionnaire][section][hh]['Township/Village']['Answer']) == False:
                for i in list(data[source][questionnaire]['Village_GPS_info'].keys()):
                    temp = data[source][questionnaire][section][hh]['Township/Village']['Answer']
                    if temp == data[source][questionnaire]['Village_GPS_info'][i]['Name']['Answer'][0]:
                        GIS_info = data[source][questionnaire]['Village_GPS_info'][i][variable]['Answer'][0]
                        return GIS_info
                    