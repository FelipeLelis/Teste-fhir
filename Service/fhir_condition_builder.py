""" Aqui temos a construção do recurso Condition, utilizamos as informações minimas para 
construção do recurso """
def condition_factory(patient_data, patient_id):
    data = {
        "resourceType": "Condition",
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/brazilian-condition"
            ]
        },
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Ativa"
                }
            ],
            "text": "Ativa"
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmada"
                }
            ],
            "text": "Confirmada"
        },
        "code": {
            "coding": [
                {
                    "system": patient_data['code_coding'],
                    "code": patient_data['code_coding_code'],
                    "display": patient_data['code_coding_display']
                }
            ],
            "text": patient_data['code_coding_display']
        },
        "subject": {
            "reference": "Patient/" + str(patient_id)
        },
        "note": [
            {
                "text": patient_data['note']
            }
        ]
    }
    return data
