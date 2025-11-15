from typing import Dict, Tuple, Optional
import random

from .util_rsa import generate_rsa_keypair as gerador_rsa_chaves, rsa_encrypt as rsa_encriptador


def make_linear_related_case(m1: int, m2: int, bits: int = 1024) -> Dict[str, int]:
    """
    Gera um caso Franklin–Reiter dado m1 e m2 numéricos.
    
    Retorna dicionário contendo:
    { n, e, d, a, b, m1, m2, c1, c2 }
    """

    # 1. Gera chave RSA
    public_key, private_key = gerador_rsa_chaves(bits)
    e, n = public_key
    d, _, _ = private_key

    # 2. Verifica que valores fornecidos cabem no módulo
    if not (0 <= m1 < n and 0 <= m2 < n):
        raise ValueError("m1 e m2 devem ser inteiros entre 0 e n-1.")

    # 3. Resolve para a e b:
    #    m2 ≡ a·m1 + b (mod n)
    # Escolhemos a ≠ 0
    a = random.randint(1, n-1)

    # Calculamos b tal que:
    #    b ≡ m2 - a·m1 (mod n)
    b = (m2 - a * m1) % n

    # 4. Calcula os cifrados
    c1 = pow(m1, e, n)
    c2 = pow(m2, e, n)

    return {
        "n": n,
        "e": e,
        "d": d,
        "a": a,
        "b": b,
        "m1": m1,
        "m2": m2,
        "c1": c1,
        "c2": c2,
    }