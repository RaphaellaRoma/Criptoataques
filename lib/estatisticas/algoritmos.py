"""
Métricas de desempenho dos algoritmos de criptografia.
"""

import time
from typing import Callable, Dict, Any
from crypto_io import texto_para_inteiro, inteiro_para_texto


def medir_tempo(func: Callable, *args, repeticoes: int = 1, **kwargs) -> float:
    """
    Mede tempo médio de execução de uma função.
    """
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        func(*args, **kwargs)
        tf = time.perf_counter()
        tempos.append(tf - t0)
    return sum(tempos) / repeticoes


def expansao_tamanho(texto_original: str, texto_cifrado: str) -> float:
    """
    Quanto maior fica o texto após a cifra.
    Retorna fator = len(cifrado)/len(original)
    """
    if len(texto_original) == 0:
        return 0
    return len(texto_cifrado) / len(texto_original)


def calcular_avalanche(func_encrypt: Callable, texto: str) -> float:
    """
    Mede o efeito avalanche comparando a cifra de:
    - texto original
    - texto com 1 caractere alterado

    Retorna % de caracteres diferentes.
    """
    if len(texto) < 1:
        return 0.0

    # cifra original
    c1 = func_encrypt(texto)

    # altera 1 caractere (primeiro)
    alterado = chr((ord(texto[0]) + 1) % 256) + texto[1:]
    c2 = func_encrypt(alterado)

    # compara diferenças
    diffs = sum(1 for a, b in zip(c1, c2) if a != b)
    max_len = max(len(c1), len(c2))

    return diffs / max_len if max_len else 0.0