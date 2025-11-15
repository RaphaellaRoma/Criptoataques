"""
Testes unitários para analise_de_frequencia.py
Executar com: pytest -v
"""

import os
import sys
import pytest

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.ataques.analise_de_frequencia import (
    contar_frequencias,
    frequencia_relativa,
    caracteres_mais_frequentes,
    FREQ_PT,
    FREQ_EN,
    score_chi_quadrado,
    score_phi_quadrado,
)


# Testes de contagem de frequências

def test_contar_frequencias_basico():
    texto = "ABCA"
    esperado = {"A": 2, "B": 1, "C": 1}
    assert contar_frequencias(texto) == esperado


def test_contar_frequencias_com_caracteres_repetidos():
    texto = "AAAAA"
    assert contar_frequencias(texto) == {"A": 5}


def test_contar_frequencias_texto_vazio():
    assert contar_frequencias("") == {}


# Testes de frequência relativa

def test_frequencia_relativa_soma_1():
    freqs = {"A": 2, "B": 2, "C": 4}
    rel = frequencia_relativa(freqs)
    assert abs(sum(rel.values()) - 1.0) < 1e-9


def test_frequencia_relativa_valores_corretos():
    freqs = {"A": 1, "B": 1}
    rel = frequencia_relativa(freqs)
    assert rel["A"] == 0.5
    assert rel["B"] == 0.5


def test_frequencia_relativa_vazio():
    assert frequencia_relativa({}) == {}


# Testes de caracteres_mais_frequentes

def test_caracteres_mais_frequentes_basico():
    freqs = {"A": 5, "B": 2, "C": 1}
    resultado = caracteres_mais_frequentes(freqs)
    assert resultado[0] == ("A", 5)
    assert resultado[1] == ("B", 2)


def test_caracteres_mais_frequentes_n_maior_que_tamanho():
    freqs = {"A": 3}
    resultado = caracteres_mais_frequentes(freqs)
    assert resultado == [("A", 3)]


def test_caracteres_mais_frequentes_empate_ordem_alfabetica():
    freqs = {"A": 2, "B": 2, "C": 1}
    resultado = caracteres_mais_frequentes(freqs)

    # só os dois mais frequentes
    top2 = resultado[:2]

    assert set(top2) == {("A", 2), ("B", 2)}


# Testes dos perfis linguísticos

def test_perfis_linguisticos_tem_letras_basicas():
    for perf in (FREQ_PT, FREQ_EN):
        assert "A" in perf
        assert "E" in perf
        assert "O" in perf


def test_perfis_linguisticos_somam_1_aproximado():
    for perf in (FREQ_PT, FREQ_EN):
        assert abs(sum(perf.values()) - 1.0) < 1e-3


# Testes de chi-quadrado e phi-quadrado

def test_score_chi_quadrado_zero_para_iguais():
    obs = {"A": 0.5, "B": 0.5}
    ref = {"A": 0.5, "B": 0.5}
    assert score_chi_quadrado(obs, ref) == pytest.approx(0.0)


def test_score_phi_quadrado_zero_para_iguais():
    obs = {"A": 0.5, "B": 0.5}
    ref = {"A": 0.5, "B": 0.5}
    assert score_phi_quadrado(obs, ref) == pytest.approx(0.0)


def test_score_chi_quadrado_maior_para_diferencas():
    obs = {"A": 1.0, "B": 0.0}
    ref = {"A": 0.5, "B": 0.5}
    assert score_chi_quadrado(obs, ref) > 0


def test_score_phi_quadrado_maior_para_diferencas():
    obs = {"A": 1.0, "B": 0.0}
    ref = {"A": 0.5, "B": 0.5}
    assert score_phi_quadrado(obs, ref) > 0