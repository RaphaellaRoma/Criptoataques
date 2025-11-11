def poly_normalize(p):
    """Remove zeros à direita e garante representação mínima."""
    if not p:
        return [0]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def poly_add(p, q):
    """Soma dois polinômios representados por listas de coeficientes."""
    n = max(len(p), len(q))
    resultado = [] 
    
    for i in range(n):
        if i < len(p) and i < len(q):
            resultado.append(p[i] + q[i])
        elif i < len(p):
            resultado.append(p[i])
        elif i < len(q):
            resultado.append(q[i])
        else:
            resultado.append(0)
    return poly_normalize(resultado)

def poly_mul(p, q):
    """Multiplica dois polinômios."""
    resultado = [0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            resultado[i + j] += p[i] * q[j]
    return poly_normalize(resultado)

def poly_eval(p, x):
    """Avalia o polinômio p em x usando Horner."""
    resultado = 0
    for coef in reversed(p):
        resultado = resultado * x + coef
    return resultado

def poly_gcd(p, q):
    """Calcula o MDC de dois polinômios usando o algoritmo de Euclides."""
    p = poly_normalize(p[:])
    q = poly_normalize(q[:])

    # Garante que q não seja o zero
    while any(q):
        # Divisão polinomial (apenas o resto)
        _, r = poly_divmod(p, q)
        p, q = q, r
    return poly_normalize(p)

def poly_divmod(p, q):
    """Divide p por q e retorna (quociente, resto)."""
    k = p[:]
    q = poly_normalize(q)
    if q == [0]:
        raise ZeroDivisionError("Divisão por polinômio nulo")

    resultado = [0] * (max(len(k) - len(q) + 1, 1))
    while len(k) >= len(q) and any(k):
        coef = k[-1]/q[-1]
        dif_grau = len(k) - len(q)
        resultado[dif_grau] = coef
        for i in range(len(q)):
            k[dif_grau + i] -= coef * q[i]
        k = poly_normalize(k)
    return (poly_normalize(resultado), poly_normalize(k))
