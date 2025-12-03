from typing import Dict, Optional, Tuple
from .util_rsa import generate_rsa_keypair as gerador_rsa_chaves, rsa_encrypt as rsa_encriptador
from crypto_io.util_io import texto_para_inteiro
import secrets

def gerar_chaves(bits: int, e_inicial: Optional[int] = None):
    if bits < 256:
        raise ValueError("bits deve ser >= 256 (use >= 1024).")

    public_key, private_key = gerador_rsa_chaves(bits, e_inicial=e_inicial)
    e, n = public_key
    d, p, q = private_key

    return n, e, d


def gerar_mensagens_relacionadas(n: int, a: Optional[int], b: Optional[int], texto: Optional[str]) -> Tuple[int, int, int, int, Optional[int]]:
    # garante a
    if a is None:
        a = secrets.randbelow(n - 1) + 1
    else:
        a = a % n
        if a == 0:
            raise ValueError("a não pode ser 0.")

    # garante b
    if b is None:
        b = secrets.randbelow(n)
    else:
        b = b % n

    nbytes = None

    # Caso 1 — passou texto: gera m1 a partir do texto
    if texto is not None:
        m1, nbytes = texto_para_inteiro(texto)
        if m1 >= n:
            raise ValueError("Texto codificado não cabe em n.")

        m2 = (a * m1 + b) % n
        if m2 == m1:
            b = (b + 1) % n
            m2 = (a * m1 + b) % n

        return m1, m2, a, b, nbytes

    # Caso 2 — Nenhum texto: m1 aleatório
    max_tries = 1000
    for _ in range(max_tries):
        m1 = secrets.randbelow(n - 2) + 2
        m2_tmp = (a * m1 + b) % n
        if m1 != m2_tmp:
            break
    else:
        raise RuntimeError("Falha ao gerar m1 != m2 após várias tentativas.")

    m2 = (a * m1 + b) % n
    return m1, m2, a, b, None


def gerar_caso_textos(texto1, texto2, bits=1024, a=None, b=None, encrypt_func=None, e_inicial: Optional[int] = None):
    n, e, d = gerar_chaves(bits, e_inicial=e_inicial)
    m1, nbytes1 = texto_para_inteiro(texto1)
    m2, nbytes2 = texto_para_inteiro(texto2)
    if m1 >= n or m2 >= n:
        raise ValueError("Texto codificado não cabe em n.")
    if a is None:
        a = secrets.randbelow(n - 1) + 1
    if b is None:
        b = (m2 - a * m1) % n
    c1 = rsa_encriptador(m1, (e, n))
    c2 = rsa_encriptador(m2, (e, n))
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
        "nbytes": (nbytes1, nbytes2)
    }


def gerar_caso_inteiros(m1, m2, bits=1024, a=None, b=None, encrypt_func=None, e_inicial: Optional[int] = None):
    n, e, d = gerar_chaves(bits, e_inicial=e_inicial)
    m1 = m1 % n
    m2 = m2 % n
    if a is None:
        a = secrets.randbelow(n - 1) + 1
    if b is None:
        b = (m2 - a * m1) % n
    c1 = rsa_encriptador(m1, (e, n))
    c2 = rsa_encriptador(m2, (e, n))
    return {
        "n": n,
        "e": e,
        "d": d,
        "a": a,
        "b": b,
        "m1": m1,
        "m2": m2,
        "c1": c1,
        "c2": c2
    }


def gerar_caso_m1(m1=None, texto1=None, bits=1024, a=None, b=None, encrypt_func=None, e_inicial: Optional[int] = None):
    n, e, d = gerar_chaves(bits, e_inicial=e_inicial)
    nbytes = None
    if texto1 is not None:
        m1, nbytes = texto_para_inteiro(texto1)
        if m1 >= n:
            raise ValueError("Texto codificado não cabe em n.")
    else:
        m1 = m1 % n
    if a is None:
        a = secrets.randbelow(n - 1) + 1
    if b is None:
        b = secrets.randbelow(n)
    m2 = (a * m1 + b) % n
    c1 = rsa_encriptador(m1, (e, n))
    c2 = rsa_encriptador(m2, (e, n))
    caso = {
        "n": n,
        "e": e,
        "d": d,
        "a": a,
        "b": b,
        "m1": m1,
        "m2": m2,
        "c1": c1,
        "c2": c2
    }
    if nbytes is not None:
        caso["nbytes"] = nbytes
    return caso


def gerar_caso_aleatorio(bits=1024, a=None, b=None, encrypt_func=None, e_inicial: Optional[int] = None):
    n, e, d = gerar_chaves(bits, e_inicial=e_inicial)
    m1, m2, a_final, b_final, nbytes = gerar_mensagens_relacionadas(n, a, b, None)
    c1 = rsa_encriptador(m1, (e, n))
    c2 = rsa_encriptador(m2, (e, n))
    caso = {
        "n": n,
        "e": e,
        "d": d,
        "a": a_final,
        "b": b_final,
        "m1": m1,
        "m2": m2,
        "c1": c1,
        "c2": c2
    }
    if nbytes is not None:
        caso["nbytes"] = nbytes
    return caso


def gerador_caso_relacionado_linear(bits=1024, a=None, b=None, texto1=None, texto2=None, m1=None, m2=None, encrypt_func=None, e_inicial=None):
    if texto1 is not None and texto2 is not None:
        return gerar_caso_textos(texto1, texto2, bits, a, b, encrypt_func, e_inicial=e_inicial) 
    elif m1 is not None and m2 is not None:
        return gerar_caso_inteiros(m1, m2, bits, a, b, encrypt_func, e_inicial=e_inicial)
    elif texto1 is not None and texto2 is None:
        return gerar_caso_m1(m1=None, texto1=texto1, bits=bits, a=a, b=b, encrypt_func=encrypt_func, e_inicial=e_inicial) 
    elif m1 is not None and m2 is None:
        return gerar_caso_m1(m1=m1, texto1=None, bits=bits, a=a, b=b, encrypt_func=encrypt_func, e_inicial=e_inicial) 
    else:
        return gerar_caso_aleatorio(bits, a, b, encrypt_func, e_inicial=e_inicial)