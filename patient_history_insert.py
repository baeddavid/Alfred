import sys
import json
import os, ibm_db, ibm_db_dbi as dbi, pandas as pd
import requests

def main(params):
    ## Database credentials
    db2_dsn = 'DATABASE={};HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;PROTOCOL=TCPIP;UID=zcx28491;PWD=Qson8p4KB19I2ONX;SECURITY=SSL'.format(
        'bludb',
        'XXXXX.databases.appdomain.cloud',
        'XXXXX',
        uid='XXXXX',
        pwd='XXXXX'
    )
    uuid = params['uuid']
    patient_name = params['patient_name']
    patient_age = params['patient_age']
    patient_gender = params['patient_gender']
    day_of_diag = params['day_of_diag']
    diag_location = params['diag_location']
    day_of_symptom = params['day_of_symptom']
    is_symptomatic = params['is_symptomatic']
    qual_of_life = params['qual_of_life']
    palpitation = params['palpitation']
    dizziness_level = params['dizziness_level']
    shortness_breathe_level = params['shortness_breathe_level']
    fatigue_level = params['fatigue_level']
    other_symptoms = params['other_symptoms']
    ekg_capture = params['ekg_capture']
    ekg_date = params['ekg_date']
    ambulatory_monitor_capture = params['ambulatory_monitor_capture']
    wearable_smart_device = params['wearable_smart_device']
    cardioversion = params['cardioversion']
    on_medication = params['on_medication']
    is_medication_effective = params['is_medication_effective']
    is_resting_heart_high = params['is_resting_heart_high']
    is_heart_high_activities = params['is_heart_high_activities']
    AF_type = params['af_type']
    paroxysmal = params['paroxysmal']
    had_heart_attack = params['had_heart_attack']
    has_angina = params['has_angina']
    has_cabg = params['has_cabg']
    has_pci = params['has_pci']
    has_pacemaker = params['has_pacemaker']
    icd = params['icd']
    has_implant_monitor = params['has_implant_monitor']
    device_age = params['device_age']
    valve_disease = params['valve_disease']
    valve_name_1 = params['valve_name_1']
    narrow_or_leak = params['narrow_or_leak']
    valve_surgery = params['valve_surgery']
    valve_name_2 = params['valve_name_2']
    repair_replacement = params['repair_replacement']
    chf = params['chf']
    hypyertension = params['hypertension']
    diabetes = params['diabetes']
    stroke = params['stroke']
    thromboembolism = params['thromboembolism']
    peripheral_vascular = params['peripheral_vascular']
    height = params['height']
    weight = params['weight']
    etoh = params['etoh']
    tob = params['tob']
    sleep_apnea = params['sleep_apnea']
    sleep_apnea_treatment = params['sleep_apnea_treatment']

    query2 = """INSERT INTO "ZCX28491"."PATIENT_HISTORY" (UUID, NAME, AGE, GENDER, DAY_AF_DIAG, AF_DIAG_LOCATION, DAY_SYMPTOM, SYMPTOMATIC, QUAL_OF_LIFE, PALPITATION, DIZZINESS, SHORTNESS_BREATHE, FATIGUE, OTHER_SYMPTOMS, EKG_CAPTURE,
    AMBULATORY_MONITOR_CAP, WEARABLE_SMART_DEV, CARDIOVERSION, MEDICATION, MEDICATION_EFFECTIVE, RESTING_HEART_HIGH, HIGH_HEART_ACTIVITIES, AF_TYPE, PAROXYSMAL, HEART_ATTACK, ANGINA, CABG, PCI, PACEMAKER, ICD, IMPLANT_MONITOR, DEVICE_AGE,
    VALVE_DISEASE, VALVE_NAME_1, NARROW_OR_LEAK, VALVE_SURGERY, VALVE_NAME_2, REPAIR_REPLACEMENT, CHF, HYPERTENSION, DIABETES, STROKE, THROMBOEMBOLISM, PERIPHERAL_VASCULAR, HEIGHT, WEIGHT, ETOH, TOB, SLEEP_APNEA, SLEEP_APNEA_TREATMENT, EKG_DATE)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    params = (uuid, patient_name, patient_age, patient_gender, day_of_diag, diag_location, day_of_symptom, is_symptomatic, qual_of_life, palpitation, dizziness_level, shortness_breathe_level, fatigue_level, other_symptoms, ekg_capture, ambulatory_monitor_capture,
              wearable_smart_device, cardioversion, on_medication, is_medication_effective, is_resting_heart_high, is_heart_high_activities, AF_type, paroxysmal, had_heart_attack, has_angina, has_cabg, has_pci, has_pacemaker, icd, has_implant_monitor, device_age,
              valve_disease, valve_name_1, narrow_or_leak, valve_surgery, valve_name_2, repair_replacement, chf, hypyertension, diabetes, stroke, thromboembolism, peripheral_vascular, height, weight, etoh, tob, sleep_apnea, sleep_apnea_treatment, ekg_date)

    ## Database connection string
    db2_connection = dbi.connect(db2_dsn)
    my_cursor = db2_connection.cursor()
    my_cursor.execute(query2, params)
    ## UNCOMMENT WHEN DONE
    ## status = db2_connection.commit()

    ## Patient history introduction
    patient_history_intro = f'{patient_name} is a {patient_age}-year-old {"man" if patient_gender == "male" else "woman" } who was diagnosed with atrial fibrillation {day_of_diag}. This was diagnosed at {diag_location}. He '

    ## Patient symptoms qualification
    adjective_symptom = ''

    ## Weighting adjectives
    symptom_weights = {'None': 0, 'Mild': 1, 'Moderate': 2, 'Severe': 3}
    ## This is the issue its returning the same value with the same key multiple times
    symptom_names = {'palpitation' : palpitation, 'dizziness': dizziness_level, 'shortness of breathe': shortness_breathe_level, 'fatigue': fatigue_level}
    symptoms = [palpitation, dizziness_level, shortness_breathe_level, fatigue_level]
    ## Weight of the adjective
    symptom_weight_total = 0
    adjective = ''
    ## Number of commas and 'and' interjection for string
    interjection = 0
    ## Number of commas and 'and' for negative interjections in denial string
    interjection_negative = 0

    ## For loop to determine the weight of the adjective and how many interjections need to be inserted into the string
    for symptom in symptoms:
        symptom_weight_total = symptom_weights[symptom] if symptom_weights[symptom] > symptom_weight_total else symptom_weight_total
        if symptom_weights[symptom] != 0:
            interjection += 1
        if symptom_weights[symptom] == 0:
            interjection_negative += 1

    ## For every n words in a list we need n - 1 interjections
    interjection -= 1
    interjection_negative -= 1
    ## Return the ajective corresponding to the weight by retrieving it from the symptom weights dictionary by indexing the value
    adjective = list(symptom_weights.keys())[list(symptom_weights.values()).index(symptom_weight_total)]

    ## Append 'ly' to the end of the adjective
    if adjective != '':
        adjective += 'ly '

    ##symptom_list = f'''{"palpitations" if palpitation != "none" else ""} {"," if interjection > 1 else ""} {"and" if interjection == 1 else ""} {"dizziness" if dizziness_level != "none" else ""}
    ##    {"shortness of breathe" if shortness_breathe_level != "none" else ""} {"fatigue" if fatigue_level != "none" else ""}'''

    ## Pointer to iterate through the array and index it
    pointer = 0
    ## Itializing the list of symptoms we want to render
    symptom_list = ""

    ## Loop until we have used all interjections
    while interjection >= 0:
        ## Iterate through the array of symptoms once
        while pointer < len(symptoms):
            ## If the symptom value is not none and interjection is greater than one, insert a comma and remove that symptom from the dictinoary
            if symptoms[pointer] != 'None' and interjection > 1:
                symptom_list = symptom_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]}, '
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            ## If the symptom value it not none and interjection is one, insert a comma and an 'and' and remove that symptom from the dictionary
            elif symptoms[pointer] != 'None' and interjection == 1:
                symptom_list = symptom_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]} and '
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            ## If the symptom is not none and interjefction is 0 we simply insert the symptom into the string and remove that symptom from the dictinary
            elif symptoms[pointer] != 'None':
                symptom_list = symptom_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]}.'
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            ## For every iteartion through the list, increment the pointer by one and decrement the interjection by one
            interjection -= 1
            pointer += 1

    ## Reinitialize the sympmtom names dictionary and pointer
    pointer = 0
    symptom_names = {'palpitation' : palpitation, 'dizziness': dizziness_level, 'shortness of breathe': shortness_breathe_level, 'fatigue': fatigue_level}
    symptom_denial_list = ''

    while interjection_negative >= 0:
        while pointer < len(symptoms):
            if pointer == 0:
                symptom_denial_list = f'{patient_name} denies any symptoms of '
            elif symptoms[pointer] == 'None' and interjection_negative > 1:
                symptom_denial_list = symptom_denial_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]}, '
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            elif symptoms[pointer] == 'None' and interjection_negative == 1:
                symptom_denial_list = symptom_denial_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]}, and'
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            elif symptoms[pointer] == 'None':
                symptom_denial_list = symptom_denial_list + f'{list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])]}. '
                symptom_names.pop(list(symptom_names.keys())[list(symptom_names.values()).index(symptoms[pointer])])
            interjection_negative -= 1
            pointer += 1

    ## Append the symptom list to the string
    adjective_symptom = f'is {adjective}symptomatic with ' + symptom_list + symptom_denial_list

    ## Patient EKG history
    patient_ekg_history = ''
    if ekg_capture == 'no':
        patient_ekg_history = 'The patient did not have an EKG done.'
    ## If the patient had an ekg done but does not remember when it was done
    elif ekg_capture == 'yes' and ekg_date == 'no':
        patient_ekg_history = 'A 12 lead EKG demonstrated atrial fibrillation. The patient does not recall last when the EKG was performed.'
    ## If the patient had an ekg and has a date when it was last performed
    else:
        patient_ekg_history = f'A 12 lead EKG {ekg_date} demonstrated atrial fibrillation.'

    ## Patient history
    patient_history = patient_history_intro + adjective_symptom + patient_ekg_history

    ## Initialize response object
    response = {}

    ## Debug lines
    response = {"history_return": patient_history}
    ## Return the response
    return response