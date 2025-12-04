import unicodedata

def remover_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def somente_letras(texto: str, alfabeto: str) -> str:
    """
    Remove tudo que não está no alfabeto indicado. 
    Usada para limpar o texto antes da análise de frequência.
    """
    
    texto_processado = remover_acentos(texto.upper())
    alfabeto_processado = remover_acentos(alfabeto.upper())

    return ''.join(c for c in texto_processado if c in alfabeto_processado)


ALFABETO_PADRAO = "ABCDEFGHIJKLMNOPQRSTUVWXyZ"

def normalizar_texto(texto, alfabeto=ALFABETO_PADRAO, remover_espacos=False) -> str:
    """
    Normaliza texto para uso geral (mantém pontuação e caracteres não-alfabéticos).
    - caixa alta
    - converte acentuadas em não-acentuadas
    - **NÃO FILTRA caracteres não-alfabéticos**
    """
    
    texto_processado = remover_acentos(texto.upper())

    if remover_espacos:
        texto_processado = texto_processado.replace(' ', '')

    return texto_processado