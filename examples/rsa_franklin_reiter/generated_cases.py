from typing import Dict, Tuple, Optional, Union
import random

from lib.ataques.rsa_franklin_reiter.util_rsa import generate_rsa_keypair as gerador_rsa_chaves
from crypto_io.util_io import texto_para_inteiro

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


def gerador_caso_m1(m1: Union[int, str], bits: int = 1024, a: Optional[int] = None, b: Optional[int] = None) -> Tuple[Optional[str], Dict[str, int]]:
    """
    Gera um caso Franklin–Reiter passando apenas m1.

    - `m1` pode ser inteiro ou texto.
    - Gera automaticamente `m2 = (a*m1 + b) mod n` (escolhendo `a` e `b` se não fornecidos).

    Retorna: (m1_original_ou_None_se_texto, caso)
    Onde `caso` tem as chaves { n, e, d, a, b, m1, m2, c1, c2 } e opcionalmente `nbytes` se `m1` for texto.
    """
    # Gera chave RSA
    public_key, private_key = gerador_rsa_chaves(bits)
    e, n = public_key
    d, p, q = private_key

    if not isinstance(bits, int):
        raise TypeError("bits deve ser um inteiro.")
    if bits < 256:
        raise ValueError("bits deve ser >= 256 (use >=1024).")

    # escolhe/valida a
    if a is None:
        a = random.randint(1, n - 1)
    else:
        if not isinstance(a, int):
            raise TypeError("a deve ser inteiro ou None.")
        a = a % n
        if a == 0:
            raise ValueError("a não pode ser 0 (mod n) na relação m2 = a*m1 + b")

    # escolhe/valida b
    if b is None:
        b = random.randint(0, n - 1)
    else:
        if not isinstance(b, int):
            raise TypeError("b deve ser inteiro ou None.")
        b = b % n

    nbytes = None
    m1_original = None
    # converte texto para inteiro se necessário
    if isinstance(m1, str):
        m1_original = m1
        m1, nbytes = texto_para_inteiro(m1)
        if m1 >= n:
            raise ValueError(
                "Texto codificado não cabe em n. Use chave maior ou divida o texto em blocos menores."
            )
    elif not isinstance(m1, int):
        raise TypeError("m1 deve ser inteiro ou texto.")

    if not (2 <= m1 < n):
        raise ValueError("m1 deve estar no intervalo [2, n-1].")

    # calcula m2 e evita igualdade
    m2 = (a * m1 + b) % n
    if m2 == m1:
        b = (b + 1) % n
        m2 = (a * m1 + b) % n

    # cifrados
    c1 = pow(m1, e, n)
    c2 = pow(m2, e, n)

    caso = {
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
    if nbytes is not None:
        caso["nbytes"] = nbytes

    return (m1_original if m1_original is not None else None, caso)