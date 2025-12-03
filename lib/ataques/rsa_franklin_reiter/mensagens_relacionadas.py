"""
- Rapha: construir_polinomio_para_cifra
- Eliane: construir_polinomio_de_relacao
- Stephany: tentar_recuperar_mensagem
"""
from math import comb
from sympy import symbols, Poly, expand
from lib.ataques.rsa_franklin_reiter.polynomial import poly_eval

def expandir_relacao_linear(a: int, b: int, e: int, c: int, n: int | None = None) -> list[int]:
    """
    Expande o polinômio (a*x + b)^e - c.

    - Se n=None, retorna coeficientes inteiros exatos.
    - Se n!=None, retorna coeficientes reduzidos módulo n.

    Retorna os coeficientes em ordem crescente:
    [c0, c1, c2, ...] representando c0 + c1*x + c2*x^2 + ...

    Args:
        a, b: relação linear m2 = a*m1 + b
        e: expoente público RSA
        c: cifra associada c2 = m2^e
        n: módulo RSA

    Returns:
        list[int]: coeficientes do polinômio.
    """

    coefs = [0] * (e + 1)

    for k in range(e + 1):
        # A base 'a' deve ser reduzida se n estiver definido.

        # a^k mod n
        if n is None:
            raise ValueError("Módulo n não pode ser None em aritmética modular.")
        ak = pow(a, k, n)
        
        # b^(e-k) mod n
        bek = pow(b, e - k, n) if n is not None else (b ** (e - k))
        
        # expansão do binômio: (a*m1 + b)^e = soma(k=0 até e) [comb(e,k) * (a*m1)^k * b^(e-k)]
        # como estamos construindo o polinômio em m1, o coeficiente do termo m1^k é:  
        coef = comb(e, k) * ak * bek 

        if n is not None:
            coef %= n 

        coefs[k] = coef

    # subtrai a cifra do termo constante
    if n is None:
        coefs[0] -= c
    else:
        coefs[0] = (coefs[0] - c) % n

    return coefs


def construir_polinomio_para_cifra(e: int, c1: int, a: int, b: int, c2: int) -> tuple[list[int], list[int]]:
    """
    Constrói dois polinômios usados no ataque Franklin–Reiter:

    - f(x) = x^e - c1
    - g(x) = (a*x + b)^e - c2

    Retorna os coeficientes em ordem crescente.

    Args:
        e: expoente público RSA
        c1: cifra da primeira mensagem
        a, b: parâmetros da relação linear m2 = a*m1 + b
        c2: cifra da segunda mensagem

    Returns:
        (f_coefs, g_coefs)
    """

    if not (isinstance(e, int) and e > 0):
        raise ValueError("e deve ser inteiro positivo.")

    # f(x)
    f_coefs = [0] * (e + 1)
    f_coefs[0] = -c1
    f_coefs[e] = 1

    # g(x)
    g_coefs = expandir_relacao_linear(a, b, e, c2, n)

    return f_coefs, g_coefs


def construir_polinomio_de_relacao(a: int, b: int, e: int, c: int, n: int) -> list[int]:
    """
    Constrói o polinômio: p(x) = (a*x + b)^e - c   (mod n)

    Usado diretamente no ataque Franklin–Reiter para encontrar m1.

    Retorna coeficientes reduzidos módulo n.

    Args:
        a, b: relação linear m2 = a*m1 + b
        e: expoente público RSA
        c: cifra da segunda mensagem
        n: módulo RSA

    Returns:
        list[int]: coeficientes do polinômio mod n
    """

    return expandir_relacao_linear(a, b, e, c, n)


# def tentativa_de_recuperacao_de_mensagem(polinomio: list[int], n: int) -> int | None: 
#     """
#     Tenta recuperar a mensagem m1 a partir do polinômio construído. 
#     Procura raízes inteiras do polinômio no intervalo [0, n-1]. 

#     """

#     for m1 in range(n): 
#         if poly_eval(polinomio, m1, n) == 0: 
#             return m1 
#     return None


from sympy import symbols, Poly, gcd

def tentativa_de_recuperacao_de_mensagem(c1: int, c2: int, a: int, b: int, e: int, n: int) -> int | None:
    """
    Recupera m1 usando o ataque Franklin–Reiter corretamente,
    via gcd de polinômios módulo n.
    """

    x = symbols('x')

    # f(x) = x^e - c1
    f = Poly(x**e - c1, x, modulus=n)

    # g(x) = (a*x + b)**e - c2
    g = Poly((a*x + b)**e - c2, x, modulus=n)

    # gcd polinomial
    d = gcd(f, g)

    # gcd deve ser linear: x - m1
    if d.degree() != 1:
        return None  # ataque falhou

    # extrair raiz do polinômio linear a*x + b
    a1, b1 = d.all_coeffs()  # [a1, b1] representando a1*x + b1

    a1 = a1 % n
    b1 = b1 % n

    # m1 = -b1 * inv(a1) mod n
    try:
        inv_a1 = pow(a1, -1, n)
    except ValueError:
        return None  # sem inverso (não deveria acontecer no ataque padrão)

    m1 = (-b1 * inv_a1) % n
    return m1
