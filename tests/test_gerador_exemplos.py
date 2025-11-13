"""
Testes unitários para gerador_exemplos.
Executar com: pytest -v
"""

import os
import pytest
import sys

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.ataques.rsa_franklin_reiter.gerador_exemplos import gerador_caso_relacionado_linear
from crypto_io.util_io import texto_para_inteiro, inteiro_para_texto

def test_gerador_retorna_campos_basicos():
    caso = gerador_caso_relacionado_linear(bits=512) 
    esperado = {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2"}
    assert set(caso.keys()) == esperado
    assert isinstance(caso["n"], int) and caso["n"] > 0
    assert 1 <= caso["a"] < caso["n"]
    assert 0 <= caso["b"] < caso["n"]
    assert 2 <= caso["m1"] < caso["n"]
    assert 0 <= caso["c1"] < caso["n"]
    assert caso["m1"] != caso["m2"]


def test_bits_invalido_typeerror():
    with pytest.raises(TypeError):
        gerador_caso_relacionado_linear(bits="1024") # bits deve ser inteiro


def test_bits_menor_valor_raise():
    with pytest.raises(ValueError):
        gerador_caso_relacionado_linear(bits=16)  # bits muito pequeno


def test_a_zero_gera_erro():
    # passar a que reduz a zero mod n deve gerar ValueError
    with pytest.raises(ValueError):
        gerador_caso_relacionado_linear(bits=512, a=0) # a não pode ser 0 mod n


def test_b_tipo_invalido():
    with pytest.raises(TypeError):
        gerador_caso_relacionado_linear(bits=512, b="boom")


# def test_gerador_funciona_com_texto():
#     texto_original = "Mensagem secreta RSA"
#     caso = gerador_caso_relacionado_linear(bits=512, texto=texto_original)

#     esperado = {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2", "nbytes"}
#     assert set(caso.keys()) == esperado

#     # descriptografa o primeiro ciphertext e coverte de volta para texto
#     m1_recuperado = pow(caso["c1"], caso["d"], caso["n"])
#     texto_decodificado = inteiro_para_texto(m1_recuperado, caso["nbytes"])
#     assert texto_decodificado == texto_original

def test_gerador_funciona_com_texto():
    print("\n=== Iniciando teste de geração com texto ===")
    texto_original = "Mensagem secreta RSA"

    caso = gerador_caso_relacionado_linear(bits=512, texto=texto_original)

    print("\n--- CHAVES GERADAS ---")
    print(f"n (bits): {caso['n'].bit_length()}")
    print(f"e = {caso['e']}")
    print(f"d = {caso['d']}\n")

    print("--- PARÂMETROS RELAÇÃO LINEAR ---")
    print(f"a = {caso['a']}")
    print(f"b = {caso['b']}\n")

    print("--- MENSAGENS ---")
    print(f"m1 = {caso['m1']}")
    print(f"m2 = {caso['m2']}")
    print(f"(m2 - a*m1 - b) mod n = {(caso['m2'] - caso['a']*caso['m1'] - caso['b']) % caso['n']}\n")

    print("--- CIFRADOS ---")
    print(f"c1 = {caso['c1']}")
    print(f"c2 = {caso['c2']}\n")

    print("--- DECODIFICAÇÃO ---")
    m1_recuperado = pow(caso["c1"], caso["d"], caso["n"])
    texto_decodificado = inteiro_para_texto(m1_recuperado, caso["nbytes"])
    print(f"Texto decodificado: {texto_decodificado}")

    esperado = {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2", "nbytes"}
    assert set(caso.keys()) == esperado
    assert texto_decodificado == texto_original

    print("=== Teste concluído com sucesso ===\n")