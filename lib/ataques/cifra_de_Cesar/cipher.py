def is_alpha_char(c: str, alfabeto: str = "abcdefghijklmnopqrstuvwxyz") -> bool:
    """Retorna True se o caractere `c` pertence ao `alfabeto`.

    >>> is_alpha_char('a')
    True
    >>> is_alpha_char('A')
    False
    >>> is_alpha_char('ç')
    False
    """
    return c in alfabeto


def normalizar_chave(chave: int, alfabeto: str = "abcdefghijklmnopqrstuvwxyz") -> int:
    """Normaliza `chave` para estar dentro do intervalo do tamanho do alfabeto.

    >>> normalizar_chave(27, 'abc')
    0
    >>> normalizar_chave(-1, 'abc')
    2
    >>> normalizar_chave(3, 'abc')
    0
    """
    n = len(alfabeto)
    return chave % n


def cifrar(texto: str, chave: int, alfabeto: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """Aplica a cifra de César sobre `texto` usando deslocamento positivo `chave`.

    Caracteres não pertencentes ao alfabeto são mantidos inalterados.

    >>> cifrar('abc', 3)
    'def'
    >>> cifrar('xyz', 3)
    'abc'
    >>> cifrar('ola mundo', 1)
    'pmb nvoep'
    """
    chave = normalizar_chave(chave, alfabeto)
    resultado = []
    for c in texto:
        if is_alpha_char(c, alfabeto):
            i = alfabeto.index(c)
            novo_i = (i + chave) % len(alfabeto)
            resultado.append(alfabeto[novo_i])
        else:
            resultado.append(c)
    return ''.join(resultado)


def decifrar(texto: str, chave: int, alfabeto: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """Desfaz a cifra de César aplicada com `chave`.

    >>> decifrar('def', 3)
    'abc'
    >>> decifrar('pmb nvoep', 1)
    'ola mundo'
    """
    chave = normalizar_chave(chave, alfabeto)
    return cifrar(texto, -chave, alfabeto)