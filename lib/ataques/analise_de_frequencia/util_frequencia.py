from typing import Dict


def contar_frequencias(texto: str, alfabeto: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> Dict[str, int]:
    """Conta frequência absoluta de cada caractere no alfabeto permitido.

    Args:
        texto: Texto a ser analisado
        alfabeto: Alfabeto permitido (padrão: A-Z)
    
    Returns:
        Dicionário com frequências absolutas de cada caractere
    """
    texto_normalizado = texto.upper()
    frequencias = {}
    
    for caractere in texto_normalizado:
        if caractere in alfabeto:
            frequencias[caractere] = frequencias.get(caractere, 0) + 1
    
    return frequencias


def frequencia_relativa(freqs: Dict[str, int]) -> Dict[str, float]:
    """Converte frequências absolutas em relativas.

    Args:
        freqs: dicionário {caractere: contagem}

    Returns:
        dicionário {caractere: frequência relativa}, somando 1.
    """
    
    if not freqs:
        return {}

    total = sum(freqs.values())
    if total == 0:
        return {}

    return {k: v / total for k, v in freqs.items()}


def caracteres_mais_frequentes(freq_rel: Dict[str, float]) -> list:
    """Retorna todos os caracteres que apareceram ordenados do mais para o menos frequente.
    
    Args:
        freq_rel: Dicionário de frequências relativas
    
    Returns:
        Lista de tuplas (caractere, frequência) ordenada por frequência decrescente
    """

    caracteres_ordenados = sorted(freq_rel.items(), key=lambda x: x[1], reverse=True)
    return caracteres_ordenados