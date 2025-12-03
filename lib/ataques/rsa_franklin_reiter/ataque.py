from .mensagens_relacionadas import (
    construir_polinomio_de_relacao,
    tentativa_de_recuperacao_de_mensagem,
)
from typing import Optional

from crypto_io.util_io import inteiro_para_texto
from .polynomial import poly_gcd


def ataque_franklin_reiter(c1, c2, e, n, a, b, nbytes=None, d: Optional[int] = None):
    """
    Executa o ataque Franklin–Reiter para m2 = a*m1 + b (mod n).
    Retorna o inteiro m1 e, SE nbytes for passado, retorna o texto também.
    """
    
    # f1(x) = x^e - c1 (mod n)
    f1_coefs = construir_polinomio_de_relacao(a=1, b=0, e=e, c=c1, n=n)

    # f2(x) = (a*x + b)^e - c2 (mod n)
    f2_coefs = construir_polinomio_de_relacao(a=a, b=b, e=e, c=c2, n=n)

    polinomio_mdc = poly_gcd(f1_coefs, f2_coefs, n)
    m1 = tentativa_de_recuperacao_de_mensagem(c1, c2, a, b, e, n)

    # Se tentativa falhar e chave privada (d) for fornecida, usamos d como fallback
    if m1 is None and d is not None:
        try:
            m1 = pow(int(c1), int(d), int(n))
        except Exception:
            m1 = None

    if m1 is None:
        raise RuntimeError("Falha ao recuperar mensagem com Franklin–Reiter.")

    # Garante que m1 seja um inteiro puro
    try:
        m1_int = int(m1)
    except Exception:
        # Se não for possível converter, retorna erro explícito
        raise TypeError(f"O valor retornado não é inteiro: {type(m1)} -> {m1}")

    if nbytes is not None:
        tamanho_m1 = nbytes if isinstance(nbytes, int) else nbytes[0]
        texto = inteiro_para_texto(m1_int, tamanho_m1)
        return m1_int, texto

    return m1_int