"""
Pacote rsa_franklin_reiter

Funções para ataque de Franklin-Reiter em RSA.
"""

from .aritmetica_modular import (
    egcd,
    modinv,
    is_probable_prime,
)

from .ataque import (
    ataque_franklin_reiter,
)

from .gerador_casos import (
    gerar_chaves,
    gerar_mensagens_relacionadas,
    gerar_caso_textos,
    gerar_caso_m1,
    gerar_caso_aleatorio,
    gerador_caso_relacionado_linear,
)

from .mensagens_relacionadas import (
    expandir_relacao_linear,
    construir_polinomio_para_cifra,
    construir_polinomio_de_relacao,
    tentativa_de_recuperacao_de_mensagem,
)

from .polynomial import (
    poly_normalize,
    poly_add,
    poly_mul,
    poly_eval,
    poly_gcd,
    poly_divmod,
)

from .util_rsa import (
    generate_prime,
    generate_rsa_keypair,
    rsa_encrypt,
    rsa_decrypt,
)

__all__ = [
    "egcd",
    "modinv",
    "is_probable_prime",
    "gerar_chaves",
    "gerar_mensagens_relacionadas",
    "gerar_caso_textos",
    "gerar_caso_m1",
    "gerar_caso_aleatorio",
    "gerador_caso_relacionado_linear",
    "expandir_relacao_linear",
    "construir_polinomio_para_cifra",
    "construir_polinomio_de_relacao",
    "tentativa_de_recuperacao_de_mensagem",
    "poly_normalize",
    "poly_add",
    "poly_mul",
    "poly_eval",
    "poly_gcd",
    "poly_divmod",
    "generate_prime",
    "generate_rsa_keypair",
    "rsa_encrypt",
    "rsa_decrypt",
]