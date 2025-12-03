"""
Funções para análise estatística geral de textos.
"""

import math
from typing import Dict
from collections import Counter

from lib.ataques.analise_de_frequencia import (
    contar_frequencias,
)


def entropia(texto: str) -> float:
    cont = Counter(texto)
    total = len(texto)
    return -sum((freq/total) * math.log2(freq/total) for freq in cont.values())

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


def autocorrelacao(texto: str, max_shift: int = 50):
    """
    Retorna lista com autocorrelação para cada shift k.
    """
    texto = texto.upper()
    nums = [ord(c) - 65 for c in texto if 'A' <= c <= 'Z']
    n = len(nums)

    R = []
    for k in range(1, max_shift + 1):
        limite = n - k
        coincid = sum(1 for i in range(limite) if nums[i] == nums[i+k])
        R.append(coincid)

    return R


def matriz_coocorrencia(texto: str, shift: int = 1):
    """
    Retorna uma matriz 26x26 onde M[a][b] é a frequência de
    letra a seguida de letra b após shift.
    """
    texto = texto.upper()
    nums = [ord(c) - 65 for c in texto if 'A' <= c <= 'Z']
    n = len(nums)

    M = [[0] * 26 for _ in range(26)]

    for i in range(n - shift):
        a = nums[i]
        b = nums[i + shift]
        M[a][b] += 1

    return M


def gerar_dados_cripto_graficos(texto_original: str, fun_cifrar, max_shift=50):
    """
    Gera:
        - texto cifrado
        - autocorrelação (lista)
        - coocorrência (matriz 26x26, shift 1)
    """
    
    cifrado = fun_cifrar(texto_original)

    dados = {
        "texto_claro": texto_original,
        "cifrado": cifrado,
        "autocorrelacao": autocorrelacao(cifrado, max_shift=max_shift),
        "coocorrencia": matriz_coocorrencia(cifrado, shift=1)
    }

    return dados