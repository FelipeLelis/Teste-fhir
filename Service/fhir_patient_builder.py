from datetime import datetime
from verify_cpf import validate_cpf

""" Aqui temos a construção estatica do recurso paciente, estaticos para motivos de teste e aprendizado
pegamos as informações do CSV fornecido e montamos o minimo aceitavel do recurso. """

def patient_factory(patient_data):
    fhir_name = patient_data.nome.split(' ')
    # Convert date string to datetime object
    date_object = datetime.strptime(
        patient_data['data de nascimento'], "%d/%m/%Y")
    # Convert datetime object to desired format
    converted_date_string = date_object.strftime("%Y-%m-%d")
    gender = ''
    if patient_data.genero == 'Masculino':
        gender = 'male'
    elif patient_data.genero == 'Feminino':
        gender = 'female'
    else:
        gender = 'other'

    # apenas verificação de cpf, como não sei se é obrigatorio, deixo um if redundante como formalidade de verificação
    cpf = ''
    result_cpf_cerify = validate_cpf(patient_data['cpf'])
    if result_cpf_cerify :
        cpf = patient_data['cpf']
    else:
        cpf = patient_data['cpf']
    data = {
        "resourceType": "Patient",
        "identifier": [
            {
                # system for example, we don't need to use this system
                "system": "https://terminology.hl7.org/CodeSystem-v2-0203",
                "value": str(cpf),
                "type": {
                    "coding": [
                        {
                            # this we need to use
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PPN",
                            "display": "CPF Number"
                        }
                    ]
                }
            }
        ],
        "name": [
            {
                "use": "official",
                "family": str(fhir_name[-1]),
                "given": [
                    fhir_name[1] if len(fhir_name[1]) > 2 else fhir_name[-1]
                ],
                "text": str(patient_data['nome'])
            }
        ],
        "gender": str(gender),
        "birthDate": str(converted_date_string),
        "telecom": [
            {
                "system": "phone",
                "value": str(patient_data['telefone']),
                "use": "home"
            }
        ],
        "birthPlace": {
            "text": str(patient_data['pais de nascimento']).capitalize(),
            "address": {
                "country": str(patient_data['pais de nascimento'])
            }
        }
    }
    return data
