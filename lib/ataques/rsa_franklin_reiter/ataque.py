from .mensagens_relacionadas import (
    construir_polinomio_de_relacao,
    tentativa_de_recuperacao_de_mensagem,
)

from crypto_io.util_io import inteiro_para_texto


def ataque_franklin_reiter(c1, c2, e, n, a, b, nbytes=None):
    """
    Executa o ataque Franklin–Reiter para m2 = a*m1 + b (mod n).
    Retorna o inteiro m1 e, SE nbytes for passado, retorna o texto também.
    """
    
    # f1(x) = x^e - c1 (mod n)
    # x = 1*x + 0
    f1_coefs = construir_polinomio_de_relacao(a=1, b=0, e=e, c=c1, n=n)

    # f2(x) = (a*x + b)^e - c2 (mod n)
    f2_coefs = construir_polinomio_de_relacao(a=a, b=b, e=e, c=c2, n=n)
    
    m1 = tentativa_de_recuperacao_de_mensagem(f1_coefs, f2_coefs, n)
    
    if m1 is None:
        raise RuntimeError("Falha ao recuperar mensagem com Franklin–Reiter.")

    
    if nbytes is not None:
        tamanho_m1 = nbytes if isinstance(nbytes, int) else nbytes[0]
        texto = inteiro_para_texto(m1, tamanho_m1)
        return m1, texto

    return m1