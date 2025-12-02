import unicodedata


def remover_acentos(texto: str) -> str:
    """
    Converte letras acentuadas em suas versões sem acento.
    """

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def somente_letras(texto: str, alfabeto: str) -> str:
    """
    Remove tudo que não está no alfabeto indicado.
    """

    texto = remover_acentos(texto.upper())
    alfabeto = remover_acentos(alfabeto.upper())

    return ''.join(c for c in texto if c in alfabeto)


ALFABETO_PADRAO = "abcdefghijklmnopqrstuvwxyz"

def normalizar_texto(texto, alfabeto=ALFABETO_PADRAO, remover_espacos=False) -> str:
    """
    Normaliza texto:
    - caixa alta
    - converte acentuadas em não-acentuadas
    - filtra caracteres usando o alfabeto
    - remove espaços (opcional)
    """
    
    texto = remover_acentos(texto.upper())

    if remover_espacos:
        texto = texto.replace(' ', '')

    texto = somente_letras(texto, alfabeto)

    return texto