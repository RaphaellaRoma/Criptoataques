from .cipher import decifrar
from lib.ataques.analise_de_frequencia import contar_frequencias, frequencia_relativa, score_chi_quadrado, FREQ_PT
from crypto_io import normalizar_texto


def ataque_cesar(texto_cifrado: str) -> dict:
    """
    Executa um ataque padrão de César por análise de frequência.
    """

    texto_norm = normalizar_texto(texto_cifrado)
    
    resultados = []

    for shift in range(26):
        texto_dec = decifrar(texto_norm, shift)
        freq_obs = frequencia_relativa(contar_frequencias(texto_dec))
        
        score = score_chi_quadrado(freq_obs, FREQ_PT)

        resultados.append((shift, score))

    melhor_shift, _ = min(resultados, key=lambda x: x[1])
    melhor_texto = decifrar(texto_norm, melhor_shift)

    return {
        "melhor_shift": melhor_shift,
        "melhor_texto": melhor_texto,
        "scores": resultados,
    }