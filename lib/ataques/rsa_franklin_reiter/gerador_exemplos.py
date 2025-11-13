from typing import Dict
from .util_rsa import generate_rsa_keypair as gerador_rsa_chaves, rsa_encrypt as rsa_encriptador
from crypto_io.util_io import texto_para_inteiro as _texto_para_inteiro
from typing import Optional
import secrets

def gerador_caso_relacionado_linear(bits: int = 1024, a: Optional[int] = None, b: Optional[int] = None,texto: Optional[str] = None,) -> Dict[str, int]:
    """
    Gera caso didático para Franklin-Reiter. 

    Retorna:
    caso contém: { 'n','e','d','a','b','m1','m2','c1','c2' }
    Se 'texto' foi fornecido também retorna 'nbytes' dentro do dicionário para decodificar.
    """

    if not isinstance(bits, int):
        raise TypeError("bits deve ser um inteiro.")
    if bits < 256:
        raise ValueError("bits deve ser >= 256 (use >=1024).")

    public_key, private_key = gerador_rsa_chaves(bits)
    e, n = public_key
    d, p, q = private_key

    if not isinstance(n, int) or n <= 3:
        raise RuntimeError("Chave RSA inválida retornada por gerador_rsa_chaves.")

    if a is None:
        a = secrets.randbelow(n - 1) + 1  # 1 <= a <= n-1
    else:
        if not isinstance(a, int):
            raise TypeError("a deve ser inteiro ou None.")
        a = a % n
        if a == 0:
            raise ValueError("a não pode ser 0 (mod n) na relação m2 = a*m1 + b")

    if b is None:
        b = secrets.randbelow(n)  # 0 <= b <= n-1
    else:
        if not isinstance(b, int):
            raise TypeError("b deve ser inteiro ou None.")
        b = b % n

    nbytes = None
    if texto is not None:
        # converte texto para inteiro e verifica se cabe em n
        m1, nbytes = _texto_para_inteiro(texto)
        if m1 >= n:
            raise ValueError(
                "Texto codificado não cabe em n. "
                "Use chave maior ou divida o texto em blocos menores."
            )
    else:
        # gera m1 aleatório no intervalo [2, n-1]
        max_tries = 1000
        for _ in range(max_tries):
            m1 = secrets.randbelow(n - 2) + 2
            m2_tmp = (a * m1 + b) % n
            if m1 != m2_tmp:
                break
        else:
            raise RuntimeError("Não foi possível gerar m1 e m2 distintos após várias tentativas.")

    if texto is not None:
        m2 = (a * m1 + b) % n
        if m2 == m1:
            # ajuste para evitar igualdade
            b = (b + 1) % n
            m2 = (a * m1 + b) % n
    else:
        m2 = (a * m1 + b) % n

    c1 = rsa_encriptador(m1, (e, n))
    c2 = rsa_encriptador(m2, (e, n))

    if not (isinstance(c1, int) and isinstance(c2, int) and 0 <= c1 < n and 0 <= c2 < n):
        raise RuntimeError("rsa_encriptador retornou ciphertext(s) inválido(s).")

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

    return caso