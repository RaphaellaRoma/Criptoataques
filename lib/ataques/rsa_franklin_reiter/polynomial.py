from .aritmetica_modular import modinv


def poly_normalize(p: list[int], n: int) -> list[int]:
    """Remove zeros à direita e garante que coeficientes estejam mod n."""
    if not p:
        return [0]
    
    p = [c % n for c in p]
    
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def poly_add(p: list[int], q: list[int], n: int) -> list[int]:
    """Soma dois polinômios MÓDULO n."""
    n_grau = max(len(p), len(q))
    resultado = [] 
    
    for i in range(n_grau):
        termo = 0
        if i < len(p):
            termo += p[i]
        if i < len(q):
            termo += q[i]
        
        resultado.append(termo % n) 

    return poly_normalize(resultado, n)


def poly_mul(p: list[int], q: list[int], n: int) -> list[int]:
    """Multiplica dois polinômios MÓDULO n."""
    resultado = [0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            resultado[i + j] = (resultado[i + j] + p[i] * q[j]) % n
            
    return poly_normalize(resultado, n)


def poly_eval(p: list[int], x: int, n: int) -> int:
    """
    Avalia o polinômio p em x MÓDULO n.

    Arguments:
        p: Lista de coeficientes do polinômio (c0, c1, c2, ...).
        x: Valor para avaliar (a potencial raiz m1).
        n: Módulo RSA.

    Returns:
        int: O resultado da avaliação p(x) mod n.
    """

    resultado = 0
    for coef in reversed(p):
        resultado = resultado * x
        resultado = resultado + coef
        resultado = resultado % n

    return resultado

def poly_gcd(p: list[int], q: list[int], n: int) -> list[int]:
    """
    Calcula o MDC de dois polinômios usando o algoritmo de Euclides, MÓDULO n.
    """

    p = poly_normalize(p[:], n) 
    q = poly_normalize(q[:], n) 

    # Garante que q não seja o zero
    while any(q):
        # Divisão polinomial (apenas o resto) MÓDULO n
        _, r = poly_divmod(p, q, n)
        p, q = q, r
        
    return poly_normalize(p, n)


def poly_divmod(p: list[int], q: list[int], n: int) -> tuple[list[int], list[int]]:
    """
    Divide p por q e retorna (quociente, resto) MÓDULO n.
    """
    k = p[:]
    q = poly_normalize(q, n)
    if q == [0]:
        raise ZeroDivisionError("Divisão por polinômio nulo")

    # CALCULA O INVERSO MODULAR do coeficiente líder do divisor (q[-1])
    try:
        q_lider_inv = modinv(q[-1], n)
    except ValueError as e:
        # Se o coeficiente líder não tiver inverso (e.g., MDC(q[-1], n) != 1), 
        # a divisão não pode ser feita em Z_n. Isso pode ser esperado em alguns ataques.
        raise RuntimeError(f"Coeficiente líder do divisor não possui inverso mod {n}.") from e

    resultado = [0] * (max(len(k) - len(q) + 1, 1))
    
    while len(k) >= len(q) and any(k):
        # Coeficiente do quociente = (coef_lider_k / coef_lider_q) mod n
        # A divisão (/) é substituída por multiplicação pelo inverso modular.
        coef = (k[-1] * q_lider_inv) % n
        
        dif_grau = len(k) - len(q)
        resultado[dif_grau] = coef
        
        # Subtrai (coef * q * x^dif_grau) de k
        for i in range(len(q)):
            # Subtração MÓDULO n: (k[i] - (coef * q[i])) % n
            termo_subtracao = (coef * q[i]) % n
            k[dif_grau + i] = (k[dif_grau + i] - termo_subtracao) % n
            
        k = poly_normalize(k, n)
        
    return (poly_normalize(resultado, n), poly_normalize(k, n))