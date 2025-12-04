"""
Testes unitários para io_utils.py
Executar com: pytest -v
"""

import os
import base64
import tempfile
import pytest
import sys

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto_io import (
    inteiro_para_bytes,
    bytes_para_inteiro,
    ler_bytes,
    escrever_bytes,
    ler_texto,
    escrever_texto,
    texto_para_inteiro,
    inteiro_para_texto,
)


# ===============================
# Testes: inteiro <-> bytes
# ===============================

def test_inteiro_para_bytes_e_reverso():
    n = 123456
    b = inteiro_para_bytes(n)
    assert isinstance(b, bytes)
    assert bytes_para_inteiro(b) == n


def test_inteiro_para_bytes_com_tamanho_fixo():
    b = inteiro_para_bytes(255, tamanho=4)
    assert len(b) == 4
    assert b.endswith(b"\xff")


def test_inteiro_para_bytes_negativo_assinado():
    b = inteiro_para_bytes(-5, tamanho=2, assinado=True)
    assert bytes_para_inteiro(b, assinado=True) == -5


def test_inteiro_para_bytes_negativo_sem_assinado():
    with pytest.raises(ValueError):
        inteiro_para_bytes(-1)


def test_bytes_para_inteiro_tipo_invalido():
    with pytest.raises(TypeError):
        bytes_para_inteiro("abc")  # deve ser bytes


# ===============================
# Testes: leitura e escrita de arquivos
# ===============================

def test_escrever_e_ler_bytes(tmp_path):
    caminho = tmp_path / "dados.bin"
    dados = b"crypto"
    escrever_bytes(str(caminho), dados)
    assert ler_bytes(str(caminho)) == dados


def test_escrever_e_ler_texto(tmp_path):
    caminho = tmp_path / "texto.txt"
    conteudo = "Criptografia"
    escrever_texto(str(caminho), conteudo)
    assert ler_texto(str(caminho)) == conteudo


def test_arquivo_inexistente():
    with pytest.raises(FileNotFoundError):
        ler_texto("nao_existe.txt")


def test_escrever_bytes_tipo_invalido(tmp_path):
    with pytest.raises(TypeError):
        escrever_bytes(tmp_path / "x", "não é bytes")


def test_escrever_texto_tipo_invalido(tmp_path):
    with pytest.raises(TypeError):
        escrever_texto(tmp_path / "y", 1234)


# ===============================
# Testes: texto <-> inteiro
# ===============================

def test_texto_para_inteiro_e_reverso():
    texto = "Teste de conversão Enaile"
    n, nbytes = texto_para_inteiro(texto)
    texto_recuperado = inteiro_para_texto(n, nbytes)
    assert texto == texto_recuperado