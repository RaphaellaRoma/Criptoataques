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
    texto_para_inteiro,
    inteiro_para_texto,
)

from .normalizador import (
    remover_acentos,
    somente_letras,
    normalizar_texto,
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
    "texto_para_inteiro",
    "inteiro_para_texto",
    "remover_acentos",
    "somente_letras",
    "normalizar_texto",
]