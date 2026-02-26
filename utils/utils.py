import re

def limpar_cnpj(cnpj: str) -> str:
    """
    Remove qualquer caractere que não seja número do CNPJ.
    
    Exemplo:
    26.580.371/0001-83 -> 26580371000183
    """
    return re.sub(r'\D', '', cnpj)

import re

def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ contendo apenas números.
    
    Exemplo:
    26580371000183 -> 26.580.371/0001-83
    """
    # Remove qualquer caractere que não seja número
    cnpj = re.sub(r'\D', '', cnpj)

    # Valida tamanho
    if len(cnpj) != 14:
        raise ValueError("CNPJ deve conter 14 dígitos.")

    # Aplica formatação
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"