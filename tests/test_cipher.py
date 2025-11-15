"""
Testes unitários para gerador_exemplos.
Executar com: pytest -v
"""

import sys
import pytest
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.ataques.cifra_de_Cesar.cipher import (
    is_alpha_char,
    normalizar_chave,
    cifrar,
    decifrar,
)

def test_is_alpha_char_basico():
    assert is_alpha_char('a') is True
    assert is_alpha_char('A') is False
    assert is_alpha_char('z') is True

def test_is_alpha_char_caracteres_invalidos():
    assert is_alpha_char('ç') is False
    assert is_alpha_char('1') is False
    assert is_alpha_char(' ') is False
    assert is_alpha_char('!') is False

def test_is_alpha_char_alfabeto_customizado():
    assert is_alpha_char('α', 'αβγ') is True
    assert is_alpha_char('δ', 'αβγ') is False

def test_normalizar_chave_basico():
    assert normalizar_chave(27, 'abc') == 0
    assert normalizar_chave(-1, 'abc') == 2
    assert normalizar_chave(3, 'abc') == 0

def test_normalizar_chave_tamanhos_diferentes():
    assert normalizar_chave(5, 'abcd') == 1
    assert normalizar_chave(-5, 'abcd') == 3

def test_normalizar_chave_zero_e_modulo():
    assert normalizar_chave(0) == 0
    assert normalizar_chave(52) == 0  # 52 % 26


def test_cifrar_basico():
    assert cifrar('abc', 3) == 'def'
    assert cifrar('xyz', 3) == 'abc'

def test_cifrar_texto_com_espacos():
    assert cifrar('ola mundo', 1) == 'pmb nvoep'

def test_cifrar_preserva_nao_alfabeticos():
    assert cifrar('a! b?', 2) == 'c! d?'

def test_cifrar_alfabeto_customizado():
    assert cifrar('αβγ', 1, 'αβγ') == 'βγα'

def test_cifrar_chave_negativa():
    assert cifrar('abc', -1) == 'zab'


def test_decifrar_basico():
    assert decifrar('def', 3) == 'abc'
    assert decifrar('pmb nvoep', 1) == 'ola mundo'

def test_decifrar_alfabeto_customizado():
    assert decifrar('βγα', 1, 'αβγ') == 'αβγ'

def test_decifrar_chave_negativa():
    assert decifrar('bcd', -1) == 'cde'

def test_decifrar_e_cifrar_reverso():
    texto = "criptografia é legal!"
    assert decifrar(cifrar(texto, 7), 7) == texto
