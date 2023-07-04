""" Verificação basica do cpf caso o mesmo for obrigatorio, em varios casos o cpf não é obrigatorio
porém deixo essa função caso precise reutilizar no projeto. """
def validate_cpf(cpf):
    # Remova todos os caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifique se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifique se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcular o primeiro dígito de verificação
    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    digit1 = (sum * 10) % 11
    if digit1 == 10:
        digit1 = 0

    # Calcular o segundo dígito de verificação
    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    digit2 = (sum * 10) % 11
    if digit2 == 10:
        digit2 = 0

    # Verifique se os dígitos de verificação correspondem
    if int(cpf[9]) == digit1 and int(cpf[10]) == digit2:
        return True
    else:
        return False
