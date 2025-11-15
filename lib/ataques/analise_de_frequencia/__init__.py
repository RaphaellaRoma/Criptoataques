"""
Pacote analise_de_frequencia

Funções e perfis linguísticos para análise de frequência
"""

from .util_frequencia import (
    contar_frequencias,
    frequencia_relativa,
    caracteres_mais_frequentes,
)
from .perfis_linguisticos import (
    FREQ_PT,
    FREQ_EN,
)
from .similaridade import (
    score_chi_quadrado,
    score_phi_quadrado,
)

__all__ = [
    "contar_frequencias",
    "frequencia_relativa",
    "caracteres_mais_frequentes",
    "FREQ_PT",
    "FREQ_EN",
    "score_chi_quadrado",
    "score_phi_quadrado",
]