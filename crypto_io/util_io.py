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


# Conversões entre inteiros e bytes

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


# conversões texto <-> inteiro

def texto_para_inteiro(texto: str) -> tuple[int, int]:
    """
    Converte texto para inteiro.
    Retorna o inteiro e o número de bytes usados.
    """
    b = texto.encode('utf-8')
    return bytes_para_inteiro(b), len(b)

def inteiro_para_texto(m: int, tamanho: int) -> str:
    """
    Converte inteiro de volta para texto, sabendo quantos bytes foram usados.
    """
    b = inteiro_para_bytes(m, tamanho)
    return b.decode('utf-8')

__all__ = [
    "inteiro_para_bytes",
    "bytes_para_inteiro",
    "ler_bytes",
    "escrever_bytes",
    "ler_texto",
    "escrever_texto",
    "texto_para_inteiro",
    "inteiro_para_texto",
]