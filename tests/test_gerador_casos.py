"""
Testes unitários para gerador_exemplos.
Executar com: pytest -v
"""

import os
import pytest
import sys

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.rsa_franklin_reiter.gerador_casos import gerador_caso_relacionado_linear
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


def test_gerador_funciona_com_texto():
    print("\n=== Iniciando teste de geração com texto ===")
    texto_original = "Mensagem secreta RSA"

    caso = gerador_caso_relacionado_linear(bits=512, texto1=texto_original)

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


def test_gerador_com_texto1_e_texto2():
    texto1 = "Mensagem A"
    texto2 = "Mensagem B"

    caso = gerador_caso_relacionado_linear(bits=512, texto1=texto1, texto2=texto2)

    assert set(caso.keys()) == {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2", "nbytes"}

    # verifica relação linear
    assert (caso["m2"] - caso["a"] * caso["m1"] - caso["b"]) % caso["n"] == 0

    m1_deco = inteiro_para_texto(pow(caso["c1"], caso["d"], caso["n"]), caso["nbytes"][0])
    m2_deco = inteiro_para_texto(pow(caso["c2"], caso["d"], caso["n"]), caso["nbytes"][1])

    assert m1_deco == texto1
    assert m2_deco == texto2


def test_gerador_com_m1_e_m2_inteiros():
    m1 = 123456
    m2 = 789012

    caso = gerador_caso_relacionado_linear(bits=512, m1=m1, m2=m2)

    assert set(caso.keys()) == {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2"}

    assert caso["m1"] == m1 % caso["n"]
    assert caso["m2"] == m2 % caso["n"]

    # verifica relação linear
    assert (caso["m2"] - caso["a"] * caso["m1"] - caso["b"]) % caso["n"] == 0


def test_gerador_com_apenas_m1_inteiro():
    m1 = 987654

    caso = gerador_caso_relacionado_linear(bits=512, m1=m1)

    assert set(caso.keys()) == {"n", "e", "d", "a", "b", "m1", "m2", "c1", "c2"}

    assert caso["m1"] == m1 % caso["n"]
    assert caso["m1"] != caso["m2"]  # relação precisa alterar


def test_gerador_com_a_fornecido():
    caso = gerador_caso_relacionado_linear(bits=512, a=5)

    assert caso["a"] == 5
    assert caso["m1"] != caso["m2"]
    assert (caso["m2"] - 5 * caso["m1"] - caso["b"]) % caso["n"] == 0


def test_gerador_com_b_fornecido():
    caso = gerador_caso_relacionado_linear(bits=512, b=123)

    assert caso["b"] == 123
    assert caso["m1"] != caso["m2"]
    assert (caso["m2"] - caso["a"] * caso["m1"] - 123) % caso["n"] == 0


def test_gerador_com_a_e_b_fornecidos():
    a = 7
    b = 55
    caso = gerador_caso_relacionado_linear(bits=512, a=a, b=b)

    assert caso["a"] == a
    assert caso["b"] == b
    assert caso["m1"] != caso["m2"]
    assert (caso["m2"] - a * caso["m1"] - b) % caso["n"] == 0
    

def test_texto_maior_que_n_garante_erro():
    texto = "A" * 10000  # vira um inteiro enorme

    with pytest.raises(ValueError):
        gerador_caso_relacionado_linear(bits=512, texto1=texto)


def test_caso_raro_m1_igual_m2_ajuste_de_b(monkeypatch):
    # força m1 = m2 simulando modulo
    def fake_randbelow(n):
        return 1  # faz m1 = 2 e b = 1: m2 = (a*m1 + b) % n = mesmo valor se a=1

    monkeypatch.setattr("secrets.randbelow", fake_randbelow)

    # força a = 1 para garantir m2 == m1
    caso = gerador_caso_relacionado_linear(bits=512, a=1)

    assert caso["m1"] != caso["m2"]  # pois o código ajusta b
    # relação ainda deve ser válida
    assert (caso["m2"] - caso["a"] * caso["m1"] - caso["b"]) % caso["n"] == 0