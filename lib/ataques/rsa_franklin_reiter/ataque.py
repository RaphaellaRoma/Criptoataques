from .mensagens_relacionadas import (
    expandir_relacao_linear,
    construir_polinomio_para_cifra,
    construir_polinomio_de_relacao,
    tentativa_de_recuperacao_de_mensagem,
)

from crypto_io.util_io import inteiro_para_texto


def ataque_franklin_reiter(c1, c2, e, n, a, b, nbytes=None):
    """
    Executa o ataque Franklin–Reiter para m2 = a*m1 + b (mod n).
    Retorna o inteiro m1 e, SE nbytes for passado, retorna o texto também.
    """

    # 1. Expandir a relação linear m2 = a*m1 + b
    A, B = expandir_relacao_linear(a, b, n)

    # 2. Construir polinômios f1(x) = x^e - c1 e f2(x) = (a*x+b)^e - c2
    f1 = construir_polinomio_para_cifra(c1, e, n)
    f2 = construir_polinomio_de_relacao(A, B, c2, e, n)

    # 3. Tentativa de recuperação usando gcd dos polinômios
    m1 = tentativa_de_recuperacao_de_mensagem(f1, f2, n)
    if m1 is None:
        raise RuntimeError("Falha ao recuperar mensagem com Franklin–Reiter.")

    # 4. Se for texto, remontar
    if nbytes is not None:
        texto = inteiro_para_texto(m1, nbytes)
        return m1, texto

    return m1