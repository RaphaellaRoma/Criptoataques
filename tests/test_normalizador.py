"""
Testes unitários para normalizador.py
Executar com: pytest -v
"""

import os
import pytest
import sys

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto_io import (
    remover_acentos,
    somente_letras,
    normalizar_texto,
)


def test_remover_acentos_basico():
    assert remover_acentos('AÇÃO') == 'ACAO'
    assert remover_acentos('Olá, MUNDO!') == 'Ola, MUNDO!'
    assert remover_acentos('ÉÉÉ') == 'EEE'


def test_remover_acentos_misturado():
    assert remover_acentos('ÁrVoRe') == 'ArVoRe'
    assert remover_acentos('coração') == 'coracao'
    assert remover_acentos('PINGÜIM') == 'PINGUIM'


def test_somente_letras_filtros():
    assert somente_letras('ABC123!', 'ABC') == 'ABC'
    assert somente_letras('Ação123!', 'ACAO') == 'ACAO'
    assert somente_letras('Olá, mundo!', 'OLAMUNDO') == 'OLAMUNDO'


def test_normalizar_texto_basico():
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert normalizar_texto('Olá, mundo!', alfabeto) == 'OLAMUNDO'
    assert normalizar_texto('Olá, mundo!', alfabeto, remover_espacos=True) == 'OLAMUNDO'
    assert normalizar_texto('Éxito!', alfabeto) == 'EXITO'


def test_normalizar_texto_com_espacos():
    alfabeto = 'ABC'
    assert normalizar_texto('A B C', alfabeto) == 'ABC'
    assert normalizar_texto('A B C', alfabeto, remover_espacos=True) == 'ABC'


def test_normalizar_texto_caracteres_invalidos():
    alfabeto = 'ABC'
    assert normalizar_texto('XYZ! A1B2C3 ?', alfabeto) == 'ABC'


def test_normalizar_texto_complexo():
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    assert normalizar_texto('ÁrVoRe ÓTIMA!!! 123', alfabeto) == 'ARVOREOTIMA'