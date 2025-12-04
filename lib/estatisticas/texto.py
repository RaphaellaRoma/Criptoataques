"""
Funções para análise estatística geral de textos.
"""

import math
from typing import Dict
from collections import Counter
import numpy as np

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


def autocorrelacao_normalizada(texto: str, max_shift: int = 50):
    texto = texto.upper()
    nums = [ord(c) - 65 for c in texto if 'A' <= c <= 'Z']
    n = len(nums)

    R = []
    for k in range(1, max_shift + 1):
        limite = n - k
        coincid = sum(nums[i] == nums[i+k] for i in range(limite))

        # valor esperado se fosse completamente aleatório
        esperado = limite * (1/26)

        # normalização para evidenciar dependência
        R.append(coincid / esperado if esperado > 0 else 0)

    return R


def matriz_original_vs_cifrada(texto_claro: str, texto_cifrado: str):
    """
    Retorna matriz 26x26 onde M[c][p] conta quantas vezes
    a letra p do plaintext virou letra c no ciphertext.
    """
    texto_claro = texto_claro.upper()
    texto_cifrado = texto_cifrado.upper()

    nums_p = [ord(c) - 65 for c in texto_claro if 'A' <= c <= 'Z']
    nums_c = [ord(c) - 65 for c in texto_cifrado if 'A' <= c <= 'Z']

    n = min(len(nums_p), len(nums_c))
    M = [[0] * 26 for _ in range(26)]

    for i in range(n):
        p = nums_p[i]
        c = nums_c[i]
        M[c][p] += 1

    return M


def gerar_dados_cripto_graficos(texto_original: str, fun_cifrar, max_shift=50):
    cifrado = fun_cifrar(texto_original)

    dados = {
        "texto_claro": texto_original,
        "cifrado": cifrado,
        "coocorrencia": matriz_coocorrencia(cifrado, shift=1),
        "autocorrelacao_normalizada": autocorrelacao_normalizada(cifrado, max_shift=max_shift),
        "mapa_original_cifrada": matriz_original_vs_cifrada(texto_original, cifrado),
    }

    return dados