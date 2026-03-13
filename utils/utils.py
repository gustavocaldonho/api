import decimal
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

def calc_total(itens: list) -> decimal.Decimal:
    total = decimal.Decimal(0)
    for r in itens:
        total += r.valor
    return total

def get_skip(page: int, size: int) -> int:
    try:
        page = int(page)
        if page < 1:
            page = 0
    except (TypeError, ValueError):
        page = 0

    try:
        size = int(size)
        if size < 1:
            size = 10
    except (TypeError, ValueError):
        size = 10

    return page*size