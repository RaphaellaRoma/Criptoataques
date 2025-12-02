"""
Funções para análise estatística geral de textos.
"""

import math
from typing import Dict

from lib.ataques.analise_de_frequencia import (
    contar_frequencias,
    frequencia_relativa,
)


def entropia(texto: str) -> float:
    contagens = contar_frequencias(texto) # Retorna um Dict[str, int]
    freq_rel = frequencia_relativa(contagens) # Retorna um Dict[str, float]
    
    return -sum(p * math.log2(p) for p in freq_rel.values() if p > 0)


def indice_coincidencia(texto: str) -> float:
    """Calcula o índice de coincidência clássico de um texto.: IC mede a probabilidade de duas letras
    escolhidas ao acaso serem iguais, bom para detectar se o texto se comporta como língua natural ou
    como texto aleatório."""

    n = len(texto)
    if n <= 1:
        return 0.0

    freq = contar_frequencias(texto)
    num = sum(f * (f - 1) for f in freq.values())
    den = n * (n - 1)
    return num / den


def tamanho_bytes(texto: str, encoding: str = "utf-8") -> int:
    """Retorna o tamanho do texto em bytes."""
    return len(texto.encode(encoding))