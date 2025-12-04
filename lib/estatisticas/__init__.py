"""
Pacote estatisticas

Funções para análise estatística geral de textos.
"""

from .algoritmos import (
    medir_tempo,
    expansao_tamanho,
    calcular_avalanche,
)

from .comparacoes import comparar_algoritmos

from .texto import (
    contar_frequencias,
    indice_coincidencia,
    tamanho_bytes,
    entropia, 
    autocorrelacao,
    matriz_coocorrencia,
    gerar_dados_cripto_graficos,
    matriz_coocorrencia_centralizada,
    matriz_original_vs_cifrada,
    autocorrelacao_normalizada


)

__all__ = [
    "medir_tempo",
    "expansao_tamanho",
    "calcular_avalanche",
    "comparar_algoritmos",
    "contar_frequencias",
    "frequencia_relativa",
    "indice_coincidencia",
    "tamanho_bytes",
    "entropia",
    "autocorrelacao"
    "matriz_coocorrencia"
    "gerar_dados_cripto_graficos",
    "matriz_coocorrencia_centralizada",
    "matriz_original_vs_cifrada",
    "autocorrelacao_normalizada"
]