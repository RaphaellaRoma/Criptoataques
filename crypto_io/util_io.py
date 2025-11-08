"""
Módulo: io_utils.py
Funções auxiliares para entrada/saída e conversão de dados binários,
hexadecimais e base64, bem como leitura e escrita de arquivos.
"""

from typing import Optional, Union
import base64
import os
import string

BytesLike = Union[bytes, bytearray, memoryview]


# Conversões entre inteiros, bytes e hexadecimal

def inteiro_para_bytes(n: int, tamanho: Optional[int] = None, ordem: str = "big", assinado: bool = False) -> bytes:
    """Converte um inteiro para bytes."""
    if not isinstance(n, int):
        raise TypeError("O valor deve ser um inteiro.")
    if n < 0 and not assinado:
        raise ValueError("Não é possível converter inteiros negativos sem 'assinado=True'.")

    if n == 0 and tamanho is None:
        return (0).to_bytes(1, byteorder=ordem, signed=assinado)

    if tamanho is None:
        # calcula o tamanho mínimo necessário
        tamanho = max(1, (n.bit_length() + 7) // 8)

    return n.to_bytes(tamanho, byteorder=ordem, signed=assinado)


def bytes_para_inteiro(b: BytesLike, ordem: str = "big", assinado: bool = False) -> int:
    """Converte bytes para um inteiro."""
    if not isinstance(b, (bytes, bytearray, memoryview)):
        raise TypeError("A entrada deve ser do tipo bytes ou similar.")
    return int.from_bytes(bytes(b), byteorder=ordem, signed=assinado)


def hex_para_bytes(s: str) -> bytes:
    """Converte uma string hexadecimal em bytes."""
    if not isinstance(s, str):
        raise TypeError("A entrada deve ser uma string hexadecimal.")
    
    # remove espaços em branco, prefixo "0x" e caracteres inválidos
    s = s.strip()
    if s.startswith(("0x", "0X")):
        s = s[2:]

    permitido = set(string.hexdigits)
    filtrado = "".join(ch for ch in s if ch in permitido)

    if not filtrado:
        raise ValueError("A string não contém caracteres hexadecimais válidos.")
    if len(filtrado) % 2 != 0:
        # adiciona um zero à esquerda se o comprimento for ímpar
        filtrado = "0" + filtrado

    return bytes.fromhex(filtrado)


def dados_para_hex(dados: Union[BytesLike, int, str], prefixo: bool = False, separador: str = "", maiusculo: bool = False) -> str:
    """Converte bytes, inteiro ou string hexadecimal em texto hexadecimal formatado."""
    if isinstance(dados, int):
        dados = inteiro_para_bytes(dados)
    elif isinstance(dados, str):
        dados = hex_para_bytes(dados)
    elif not isinstance(dados, (bytes, bytearray, memoryview)):
        raise TypeError("O argumento deve ser int, bytes ou string hexadecimal.")

    h = bytes(dados).hex()

    if separador:
        h = separador.join(h[i:i + 2] for i in range(0, len(h), 2))
    if maiusculo:
        h = h.upper()
    if prefixo:
        h = "0x" + h

    return h


# Leitura e escrita de arquivos

def ler_bytes(caminho: str) -> bytes:
    """Lê um arquivo binário e retorna seu conteúdo em bytes."""
    try:
        with open(caminho, "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    except OSError as e:
        raise OSError(f"Erro ao ler o arquivo {caminho}: {e}")


def escrever_bytes(caminho: str, dados: BytesLike) -> None:
    """Escreve bytes em um arquivo (cria diretórios se necessário)."""
    if not isinstance(dados, (bytes, bytearray, memoryview)):
        raise TypeError("Os dados devem ser do tipo bytes ou similar.")
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "wb") as f:
        f.write(bytes(dados))


def ler_texto(caminho: str, codificacao: str = "utf-8") -> str:
    """Lê o conteúdo de um arquivo de texto."""
    try:
        with open(caminho, "r", encoding=codificacao) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    except OSError as e:
        raise OSError(f"Erro ao ler o arquivo {caminho}: {e}")


def escrever_texto(caminho: str, texto: str, codificacao: str = "utf-8") -> None:
    """Escreve texto em um arquivo (cria diretórios se necessário)."""
    if not isinstance(texto, str):
        raise TypeError("O conteúdo deve ser uma string.")
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", encoding=codificacao) as f:
        f.write(texto)


# Base64 e exibição em hexdump

def codificar_base64(dados: BytesLike) -> str:
    """Codifica bytes em Base64 (ASCII)."""
    if not isinstance(dados, (bytes, bytearray, memoryview)):
        raise TypeError("Os dados devem ser bytes ou similares.")
    return base64.b64encode(bytes(dados)).decode("ascii")


def decodificar_base64(s: str) -> bytes:
    """Decodifica uma string Base64 para bytes."""
    if not isinstance(s, str):
        raise TypeError("A entrada deve ser uma string Base64.")
    return base64.b64decode(s)


def exibir_hexdump(dados: BytesLike, largura: int = 16) -> str:
    """Gera um hexdump simples (offset, bytes em hexadecimal e caracteres ASCII)."""
    if not isinstance(dados, (bytes, bytearray, memoryview)):
        raise TypeError("Os dados devem ser bytes ou similares.")
    b = bytes(dados)
    linhas = []
    for offset in range(0, len(b), largura):
        bloco = b[offset:offset + largura]
        hex_bytes = " ".join(f"{c:02x}" for c in bloco)
        ascii_parte = "".join(chr(c) if 32 <= c < 127 else "." for c in bloco)
        linhas.append(f"{offset:08x}  {hex_bytes:<{largura*3}}  |{ascii_parte}|")
    return "\n".join(linhas)


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