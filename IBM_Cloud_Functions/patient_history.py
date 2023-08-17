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
        uid='XXXXXXX',
        pwd='XXXXXXX'
    )


    ## Database connection string
    db2_connection = dbi.connect(db2_dsn)

    ## SQL SELECT query
    query = 'SELECT * FROM "ZCX28491"."PATIENT_HISTORY"'

    ## Execute sql in database
    history_df = pd.read_sql_query(query, con=db2_connection)

    ## Defining params for sql query
    uuid = params['uuid']
    ## Initialize response object
    response = {}

    ## Query response
    query_df = history_df[history_df.UUID == uuid]
    ## If query returned nothing
    if query_df.shape[0] <= 0:
        response = {"Error" : "There are no records available with this data"}
    ## Query found a match
    else:
        log_string = ""
        for word in params:
            log_string = log_string + word + " "

        patient_name = query_df.NAME.item()
        patient_age = query_df.AGE.item()
        patient_gender = query_df.GENDER.item()
        day_of_diag = query_df.DAY_AF_DIAG.item()
        AF_diag_location = query_df.AF_DIAG_LOCATION.item()
        day_of_symptom = query_df.DAY_SYMPTOM.item()
        is_symptomatic = query_df.SYMPTOMATIC.item()
        qual_of_life = query_df.QUAL_OF_LIFE.item()
        palpitation = query_df.PALPITATION.item()
        dizziness_level = query_df.DIZZINESS.item()
        shortness_breathe_level = query_df.SHORTNESS_BREATHE.item()
        fatigue_level = query_df.FATIGUE.item()
        other_symptoms = query_df.OTHER_SYMPTOMS.item()
        ekg_capture = query_df.EKG_CAPTURE.item()
        ambulatory_monitor_capture = query_df.AMBULATORY_MONITOR_CAP.item()
        wearable_smart_device = query_df.WEARABLE_SMART_DEV.item()
        cardioversion = query_df.CARDIOVERSION.item()
        on_medication = query_df.MEDICATION.item()
        is_medication_effective = query_df.MEDICATION_EFFECTIVE.item()
        is_resting_heart_high = query_df.RESTING_HEART_HIGH.item()
        is_heart_high_activities = query_df.HIGH_HEART_ACTIVITIES.item()
        AF_type = query_df.AF_TYPE.item()
        paroxysmal = query_df.PAROXYSMAL.item()
        had_heart_attack = query_df.HEART_ATTACK.item()
        has_angina = query_df.ANGINA.item()
        has_cabg = query_df.CABG.item()
        has_pci = query_df.PCI.item()
        has_pacemaker = query_df.PACEMAKER.item()
        icd = query_df.ICD.item()
        has_implant_monitor = query_df.IMPLANT_MONITOR.item()
        device_age = query_df.DEVICE_AGE.item()
        valve_disease = query_df.VALVE_DISEASE.item()
        valve_name_1 = query_df.VALVE_NAME_1.item()
        narrow_or_leak = query_df.NARROW_OR_LEAK.item()
        valve_surgery = query_df.VALVE_SURGERY.item()
        valve_name_2 = query_df.VALVE_NAME_2.item()
        repair_replacement = query_df.REPAIR_REPLACEMENT.item()
        chf = query_df.CHF.item()
        hypyertension = query_df.HYPERTENSION.item()
        diabetes = query_df.DIABETES.item()
        stroke = query_df.STROKE.item()
        thromboembolism = query_df.THROMBOEMBOLISM.item()
        peripheral_vascular = query_df.PERIPHERAL_VASCULAR.item()
        height = query_df.HEIGHT.item()
        weight = query_df.WEIGHT.item()
        etoh = query_df.ETOH.item()
        tob = query_df.TOB.item()
        sleep_apnea = query_df.SLEEP_APNEA.item()
        sleep_apnea_treatment = query_df.SLEEP_APNEA_TREATMENT.item()


        response = {"history_return": query_df.NAME.item() + str(patient_age) + patient_gender + day_of_diag + AF_diag_location + day_of_symptom + str(is_symptomatic) + qual_of_life + palpitation + dizziness_level + shortness_breathe_level + fatigue_level +
                    other_symptoms + str(ekg_capture) + ambulatory_monitor_capture + wearable_smart_device + cardioversion + str(on_medication) + str(is_medication_effective) + str(is_resting_heart_high) + str(is_heart_high_activities) + AF_type + paroxysmal + str(had_heart_attack) + str(has_angina) +
                    str(has_cabg) + str(has_pci) + str(has_pacemaker) + str(icd) + str(has_implant_monitor) + str(device_age) + str(valve_disease) + valve_name_1 + narrow_or_leak + str(valve_surgery) + valve_name_2 + repair_replacement + str(chf) + str(hypyertension) + str(diabetes) + str(stroke) +
                    str(thromboembolism) + str(peripheral_vascular) + str(height) + str(weight) + etoh + tob + str(sleep_apnea) + str(sleep_apnea_treatment)}
    ## Return the response
    return response
