"""
Pacote cifra_de_Cesar

Funções para ataque de Cifra de César.
"""

from .ataque import (
    ataque_cesar,
)

from .cipher import (
    is_alpha_char,
    normalizar_chave,
    cifrar,
    decifrar,
)

from .cli import (
    ler_arquivo_texto,
    montar_parser,
    imprimir_resultados,
    main,
)

__all__ = [
    "ataque_cesar",
    "is_alpha_char",
    "normalizar_chave",
    "cifrar",
    "decifrar",
    "ler_arquivo_texto",
    "montar_parser",
    "imprimir_resultados",
    "main",
]