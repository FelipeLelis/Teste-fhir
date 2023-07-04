""" Aqui temos a criação do recurso Observation, adicionamos os dados para construção minima 
do recurso em questão. """
def observation_factory(patient_data, patient_id):
    data = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": patient_data['category_system'],
                        "code": patient_data['category_code'],
                        "display": patient_data['category_display']
                    }
                ],
                "text": patient_data['category_display']
            }
        ],
        "code": {
            "coding": [
                {
                    "system": patient_data['code_coding_system'],
                    "code": patient_data['code_coding_code'],
                    "display": patient_data['code_coding_display']
                }
            ],
            "text": patient_data['code_coding_display']
        },
        "subject": {
            "reference": "Patient/" + str(patient_id)
        },
        "valueString": patient_data['value_string']
    }

    return data
