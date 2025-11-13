"""
- Rapha: construir_polinomio_para_cifra
- Eliane: construir_polinomio_de_relacao
- Stephany: tentar_recuperar_mensagem
"""
from math import comb

def construir_polinomio_de_relacao(a: int, b: int, e: int, c: int, n: int) -> list[int]:
    """
    Constrói o polinômio que expressa a relação entre duas mensagens cifradas
    no ataque de franklin reiter. Seja m2 = a*m1 + b -> (a*m1 + b)^e = c (mod n)
    Polinômio representa p(x) = (a*x + b)^e - c (mod n)
    Retorna os coeficientes do polinômio em ordem crescente de grau.
    Ex.: [c0, c1, c2, ...] representa c0 + c1*x + c2*x^2 + ...
    
    Arguments:
        a: coeficiente da relação linear m2 = a*m1 + b
        b: constante da relação linear m2 = a*m1 + b
        e: expoente público RSA
        c: cifra da segunda mensagem (c2 = m2^e mod n)
        n: módulo RSA
    
    Returns:
       list[int]: Lista de coeficientes do polinômio reduzido módulo n
    """
    
    # inicializa polinômio de grau e
    polinomio = [0] * (e + 1)
    
    # calcula coeficientes usando binômio de Newton
    for k in range(e + 1):
        coef_binomial = comb(e, k)

        # expansão do binômio: (a*m1 + b)^e = soma(k=0 até e) [comb(e,k) * (a*m1)^k * b^(e-k)]
        # como estamos construindo o polinômio em m1, o coeficiente do termo m1^k é:
        coef = (coef_binomial * pow(a, k, n) * pow(b, e - k, n)) % n
        polinomio[k] = coef
    
    polinomio[0] = (polinomio[0] - c) % n
    
    return polinomio