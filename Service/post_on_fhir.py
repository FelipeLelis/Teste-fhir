import requests
import json

""" Temos aqui o serivço que fazer um request post no hapi fhir, ele recebe o path como caminho para saber em qual datastore
do hapifhir o recurso deve ir. Obs: O path e o tipo de recurso deve ser o mesmo, caso contrario ele não é validado 
pelo serviço hapifhir """

def post(data, path):
    fhir_url = 'http://localhost:8080/fhir/' + str(path)
    headers = {
        'Content-Type': 'application/json'
    }
    print(fhir_url)
    # Converter o recurso em JSON
    observation_json = json.dumps(data)

    # Realizar a solicitação POST
    response = requests.post(fhir_url, headers=headers, data=observation_json)

    # Verificar o código de status da resposta
    if response.status_code == 201:
        print(f"{path} criado com sucesso!")
        response_get_fhir = json.loads(response.text)
        return response_get_fhir['id']
    else:
        print(f"Erro ao criar a {path}. Código de status:", response.status_code)
        return False
