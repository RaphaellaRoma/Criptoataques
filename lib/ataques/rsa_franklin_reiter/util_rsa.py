# geração de par de chaves; encriptação; decriptação...

import random
from .aritmetica_modular import egcd, modinv, is_probable_prime


def generate_prime(bits: int):
    """
    Gera um número primo aleatório com 'bits' bits.
    Usa o teste probabilístico de Miller-Rabin.
    """
    while True:
        # garante número ímpar com bit mais significativo = 1
        p = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_probable_prime(p):
            return p


def generate_rsa_keypair(bits: int = 16, e_inicial: int | None = None):
    """
    Gera um par de chaves RSA.
    
    Args:
        bits: Tamanho da chave (em bits).
        e_inicial: Expoente público a ser usado. Se None, usa 65537.
    """
    # Gera dois primos distintos
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    N = p * q
    phi = (p - 1) * (q - 1)

    e = e_inicial if e_inicial is not None else 65537 

    g, _, _ = egcd(e, phi)
    if g != 1:
        print(f"Aviso: O expoente e={e} não é coprimo de phi. Gerando um novo...")
        while True:
            e = random.randrange(3, phi, 2)
            g, _, _ = egcd(e, phi)
            if g == 1:
                break

    # Calcula d
    d = modinv(e, phi)

    public_key = (e, N)
    private_key = (d, p, q)
    return public_key, private_key


def rsa_encrypt(m: int, public_key: tuple[int, int]) -> int:
    """
    Cifra a mensagem inteira m com a chave pública (e, N):
      c = m^e mod N
    """
    e, N = public_key
    if not (0 <= m < N):
        raise ValueError("Mensagem m deve estar no intervalo [0, N)")
    return pow(m, e, N)


def rsa_decrypt(c: int, private_key: tuple[int, int, int]) -> int:
    """
    Decifra o inteiro c com a chave privada (d, p, q):
      m = c^d mod N
    (Usado apenas para validar testes, não para o ataque.)
    """
    d, p, q = private_key
    N = p * q
    return pow(c, d, N)


# Teste rápido
if __name__ == "__main__":
    pub, priv = generate_rsa_keypair(bits=12)
    e, N = pub
    d, p, q = priv

    print("p =", p)
    print("q =", q)
    print("N =", N)
    print("e =", e)
    print("d =", d)

    m = 42
    c = rsa_encrypt(m, pub)
    print("c =", c)
    print("m decifrado =", rsa_decrypt(c, priv))
