import chardet
from pyspark.sql import SparkSession
from pyspark.sql import Row
from unidecode import unidecode
from fhir_observation_builder import observation_factory
from fhir_patient_builder import patient_factory
from fhir_condition_builder import condition_factory
from post_on_fhir import post
import time

""" Todos esses dados aqui estaticos precisam vir de uma terminilogia pre definida pela instituição em questão, 
precisariamos ter um documento fhir chamado "terminologia" onde mapeamos tudo que se faz necessario nos recursos utilizados. """

""" 
    Foram utilizadas as terminologias brasileiras para conversão do recurso e adequação a saude brasileira.
    utilizado loinc: https://loinc.org/international/portuguese/ que tem como cordenação :
        - ANS - Agência Nacional de Saúde Suplementar - Ministério da Saúde
        - SMS-SP - Secretaria Municipal de Saúde de São Paulo
        - ABRAMED - Associação Brasileira de Medicina Diagnostica
        - SBPC/ML - Sociedade Brasileira de Patologia Clinica/Medicina Laboratorial
        - SBAC - Sociedade Brasileira de Análises Clínicas - CB -36 - ABNT
        - DASA - Diagnósticos da América SA
        - Grupo Fleury SA
        - HIAE - LAB - Laboratório do Hospital Israelita Albert Einstein
        - HL7 BRASIL - Instituto HL7 Brasil
        - SBIS - Sociedade Brasileira de Informática em Saúde

    Também utilizamos o SNOMED.
        - O SNOMED-CT é uma nomenclatura clínica importante para a assistência de enfermagem e 
        utilização dos sistemas de classificação, abrindo caminho para a disseminação do registro eletrônico e da 
        integração dos diferentes níveis de atenção do Sistema Único de Saúde (SUS).
    Os codeSystems da termonologia HL7 em alguns casos pode ser mantida por ter o mesmo proposito.

"""
hypertensive_observation_code_list = {
    'category_system': 'http://terminology.hl7.org/CodeSystem/observation-category',
    'category_code': 'vital-signs',
    'category_display': 'Vital Signs',
    'code_coding_system': 'http://loinc.org',
    'code_coding_code': '55284-4',
    'code_coding_display': 'Pressão Arterial',
    'value_string': 'Hipertenso'
}

hypertensive_condition_code_list = {
    'code_coding': 'http://snomed.info/sct',
    'code_coding_code': '38341003',
    'code_coding_display': 'Hipertensão arterial',
    'note': 'Histórico de pressão arterial elevada. '
}

pregnant_observation_code_list = {
    'category_system': 'http://terminology.hl7.org/CodeSystem/observation-category',
    'category_code': 'vital-signs',
    'category_display': 'Vital Signs',
    'code_coding_system': 'http://loinc.org',
    'code_coding_code': '82810-3',
    'code_coding_display': 'Gestação',
    'value_string': 'Grávida'
}

pregnant_condition_code_list = {
    'code_coding': 'http://hl7.org/fhir/STU3/valueset-condition-code.html',
    'code_coding_code': '118185006',
    'code_coding_display': 'Gestação',
    'note': 'Paciente grávida no 1 mês'
}
diabetic_observation_code_list = {
    'category_system': 'http://terminology.hl7.org/CodeSystem/observation-category',
    'category_code': 'laboratory',
    'category_display': 'Laboratory',
    'code_coding_system': 'http://loinc.org',
    'code_coding_code': '4548-4',
    'code_coding_display': 'Glicemia em jejum',
    'value_string': 'Diabético'
}

diabetic_condition_code_list = {
    'code_coding': 'http://snomed.info/sct',
    'code_coding_code': '44054006',
    'code_coding_display': 'Diabetes mellitus',
    'note': 'Paciente diagnosticado com diabetes tipo 2.'
}


def start(path: str):
    csv_reader(path)

def verify_and_post_observations(patient_data, patient_id):
    """ percorremos as observações do paciente
    Precisamos de dois recursos para informar o fhir, a Observação(Observation) que é a sequência de atendimento que o paciente está tendo
    e Condição(Condition) que na verdade informa qual "problema" o paciente tem """
    for item in patient_data['observacao']:
        if item == 'Gestante':
            # Criando um recurso observation
            result_pregnant_observation = observation_factory(
                pregnant_observation_code_list, patient_id)
            #Criando um recurso Condition
            result_pregnant_condition = condition_factory(
                pregnant_condition_code_list, patient_id)
            # Postando recursos no Fhir
            post(result_pregnant_observation, 'Observation')
            post(result_pregnant_condition, 'Condition')
        elif item == 'Diabético':
            # Criando um recurso observation
            result_diabect_observation = observation_factory(
                diabetic_observation_code_list, patient_id)
            #Criando um recurso Condition
            result_diabetic_condition = condition_factory(
                diabetic_condition_code_list, patient_id)
            # Postando recursos no Fhir
            post(result_diabect_observation, 'Observation')
            post(result_diabetic_condition, 'Condition')
        elif item == 'Hipertenso':
            # Criando um recurso observation
            result_hypertensive_observation = observation_factory(
                hypertensive_observation_code_list, patient_id)
            #Criando um recurso Condition
            result_hypertensive_condition = condition_factory(
                hypertensive_condition_code_list, patient_id)
            # Postando recursos no Fhir
            post(result_hypertensive_observation, 'Observation')
            post(result_hypertensive_condition, 'Condition')

def create_patient_on_fhir(patient_data):
    # retorna o resultado da criação do documento fhir
    patient_result_data = patient_factory(patient_data)
    # criamos o paciente em fhir e retornamos seu id
    id_patient = post(patient_result_data, 'Patient')
    # vamos verificar se o paciente tem observações
    if id_patient :
        verify_and_post_observations(patient_data, id_patient)
    else :
        print('Erro ao criar paciente, mandando para reciclagem ... ')
        recycle(patient_data)

def treat_data_to_fhir_pattern(converted_row):
    # Separe por '|' as observações do paciente
    result_observacao = str(converted_row.observacao).split('|')
    row_dict = converted_row.asDict()
    # adicione as observações do paciente de volta ao dicionário
    row_dict['observacao'] = result_observacao
    new_converted_row = Row(**row_dict)
    # enviamos os dados carregados do csv para a "fábrica" ​​do paciente
    create_patient_on_fhir(new_converted_row)

def process_rdd(rdd):
    # Sim, estamos jogando tudo em memoria, mas isso só para questão do teste.
    for row in rdd.collect():
        # Converta as chaves de linha para minúsculas e remova os acentos
        try:
            converted_row = Row(
            **{unidecode(k.lower()): v for k, v in row.asDict().items()})
            treat_data_to_fhir_pattern(converted_row)
        finally:
            print("Ok.")
            # Sleep só para acompanhar os logs, funciona sem o sleep que passa a fazer a carga muito mais rápida
            time.sleep(1)
        
def recycle(patient_row):
    # Aqui podemos tratar possiveis registros com erro, mandando para alguma mensageria e etc ... 
    print('Reciclando', patient_row)

def treat_code_encoding(path: str) -> str:
    # Define o caminho para o arquivo CSV
    # Lê os primeiros bytes do arquivo para detecção de codificação
    with open(path, "rb") as f:
        # Lendo os primeiros 1000 bytes (ajuste conforme necessário)
        raw_data = f.read(1000)
        resultado = chardet.detect(raw_data)

    # exibir o resultado
    codificacao = resultado["encoding"]
    return codificacao

def csv_reader(path: str):
    # Criando um sessão do Spark
    spark = SparkSession.builder.appName("Reading patients").getOrCreate()
    encoded_csv_type = treat_code_encoding(path)
    # Leia o arquivo CSV em um DataFrame
    df = spark.read.csv(path, header=True, inferSchema=True,
                        encoding=encoded_csv_type)
    """ convertendo o DataFrame em um RDD (Resilient Distributed Dataset),
    você pode aproveitar os recursos de iteração do RDD. No entanto,
    observe que a conversão para um RDD pode afetar o desempenho e pode não ser necessária para todos os casos de uso. """
    rdd = df.rdd
    process_rdd(rdd)
    # Parar a sessão do spark
    spark.stop()

# inicia todo o processo 
start("./data/patients.csv")
