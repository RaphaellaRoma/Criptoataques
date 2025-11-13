# mdc_estendido; inverso_modular; eh_primo_probabilistico...

import random

# Algoritmo Estendido de Euclides
def egcd(a: int, b: int):
    """
    Algoritmo estendido de Euclides.
    Retorna uma tupla (g, x, y) tal que:
        a*x + b*y = g = gcd(a, b)
    """
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = egcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)


# Inverso Modular
def modinv(a: int, n: int):
    """
    Calcula o inverso modular de a módulo n.
    Retorna x tal que (a * x) % n == 1, se existir.
    Lança ValueError se o inverso não existir.
    """
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError(f"Inverso modular não existe para a={a}, n={n}")
    return x % n


# Teste de Primalidade (Miller–Rabin)
def is_probable_prime(n: int, k: int = 10):
    """
    Teste probabilístico de primalidade de Miller–Rabin.
    Retorna True se n for provavelmente primo, False se composto.
    
    Parâmetros:
      n: número a ser testado
      k: número de iterações (maior k = mais precisão)
    """
    # Casos triviais
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p

    # Escreve n-1 = 2^r * d, com d ímpar
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Testes aleatórios
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True