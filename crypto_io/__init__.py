"""
Pacote crypto_io

Funções auxiliares para entrada/saída e conversões
"""

from .util_io import (
    inteiro_para_bytes,
    bytes_para_inteiro,
    dados_para_hex,
    hex_para_bytes,
    ler_bytes,
    escrever_bytes,
    ler_texto,
    escrever_texto,
    codificar_base64,
    decodificar_base64,
    exibir_hexdump,
)

__all__ = [
    "inteiro_para_bytes",
    "bytes_para_inteiro",
    "dados_para_hex",
    "hex_para_bytes",
    "ler_bytes",
    "escrever_bytes",
    "ler_texto",
    "escrever_texto",
    "codificar_base64",
    "decodificar_base64",
    "exibir_hexdump",
]