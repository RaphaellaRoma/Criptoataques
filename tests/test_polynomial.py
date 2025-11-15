"""
Testes unitários para io_utils.py
Executar com: pytest -v
"""

import sys
import pytest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.ataques.rsa_franklin_reiter.polynomial import (
    poly_normalize, poly_add, poly_mul,
    poly_eval, poly_divmod, poly_gcd
)


def test_poly_normalize_basico():
    assert poly_normalize([1, 2, 0, 0]) == [1, 2]

def test_poly_normalize_zero():
    assert poly_normalize([0, 0, 0]) == [0]

def test_poly_normalize_vazio():
    assert poly_normalize([]) == [0]

def test_poly_add_tamanhos_iguais():
    assert poly_add([1, 2], [3, 4]) == [4, 6]

def test_poly_add_tamanhos_diferentes():
    assert poly_add([1, 2, 3], [5, 6]) == [6, 8, 3]

def test_poly_add_com_zero():
    assert poly_add([1, 2], [0]) == [1, 2]

def test_poly_mul_basico():
    # (1 + 2x) * (3 + 4x) = 3 + 10x + 8x²
    assert poly_mul([1, 2], [3, 4]) == [3, 10, 8]

def test_poly_mul_por_zero():
    assert poly_mul([1, 2, 3], [0]) == [0]

def test_poly_mul_identidade():
    assert poly_mul([1, 2], [1]) == [1, 2]

def test_poly_eval_basico():
    # 1 + 2x + 3x² evaluated at x=2 → 1 + 4 + 12 = 17
    assert poly_eval([1, 2, 3], 2) == 17

def test_poly_eval_zero():
    assert poly_eval([0], 10) == 0

def test_poly_eval_constante():
    assert poly_eval([5], 77) == 5

def test_poly_divmod_simples():
    # (x^2 - 1) / (x - 1) → quociente = x + 1, resto = 0
    p = [-1, 0, 1]   # -1 + 0x + 1x²
    q = [-1, 1]      # -1 + x
    quoc, rest = poly_divmod(p, q)
    assert quoc == [ 1.0, 1.0 ]  # x + 1
    assert rest == [0]

def test_poly_divmod_resto():
    # (x² + 1) / (x + 1)
    p = [1, 0, 1]
    q = [1, 1]
    quoc, rest = poly_divmod(p, q)
    # quoc = x - 1, rest = 2
    assert quoc == [-1.0, 1.0]
    assert rest == [2]

def test_poly_divmod_por_zero():
    with pytest.raises(ZeroDivisionError):
        poly_divmod([1, 2], [0])

def test_poly_gcd_mesmo_poly():
    assert poly_gcd([1, 2, 3], [1, 2, 3]) == [1, 2, 3]

def test_poly_gcd_simples():
    # gcd(x² - 1, x - 1) = x - 1
    p = [-1, 0, 1]
    q = [-1, 1]
    assert poly_gcd(p, q) == [-1, 1]

def test_poly_gcd_com_zero():
    assert poly_gcd([1, 2, 3], [0]) == [1, 2, 3]

def test_poly_gcd_zero_reverso():
    assert poly_gcd([0], [1, 2]) == [1, 2]
