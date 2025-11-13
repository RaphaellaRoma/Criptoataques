"""
- Rapha: construir_polinomio_para_cifra
- Eliane: construir_polinomio_de_relacao
- Stephany: tentar_recuperar_mensagem
"""
from math import comb
from sympy import symbols, Poly, expand
def construir_polinomio_para_cifra(e: int, c1: int, a: int, b: int, c2: int) -> tuple[list[int], list[int]]:
    """
    Constrói os polinômios que representam a relação entre mensagens e cifras:
    - f(x) = x^e - c1 (primeira mensagem cifrada)
    - g(x) = (a*x + b)^e - c2 (segunda mensagem cifrada com relação linear)
    
    Retorna os coeficientes de ambos os polinômios em ordem crescente de grau.
    Ex.: [c0, c1, c2, ...] representa c0 + c1*x + c2*x^2 + ...
    
    Arguments:
        e: expoente público RSA
        c1: cifra da primeira mensagem (c1 = m1^e)
        a: coeficiente da relação linear m2 = a*m1 + b
        b: constante da relação linear m2 = a*m1 + b
        c2: cifra da segunda mensagem (c2 = m2^e)
    
    Returns:
        tuple[list[int], list[int]]: (coeficientes_f, coeficientes_g)
    """
    if not (isinstance(e, int) and e > 0):
        raise ValueError("e deve ser inteiro positivo.")
    
    # Inicializa polinômios de grau e
    f_coefs = [0] * (e + 1)
    g_coefs = [0] * (e + 1)
    
    # f(x) = x^e - c1
    # Coeficientes: [−c1, 0, 0, ..., 1] (termo constante -c1, termo de grau e é 1)
    f_coefs[0] = -c1
    f_coefs[e] = 1
    
    # g(x) = (a*x + b)^e - c2
    # Usa binômio de Newton: (a*x + b)^e = soma(k=0 até e) [comb(e,k) * (a*x)^k * b^(e-k)]
    for k in range(e + 1):
        coef_binomial = comb(e, k)
        # Coeficiente do termo x^k é: comb(e,k) * a^k * b^(e-k)
        g_coefs[k] = coef_binomial * (a ** k) * (b ** (e - k))
    
    # Subtrai c2 do termo constante
    g_coefs[0] -= c2
    
    return f_coefs, g_coefs





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