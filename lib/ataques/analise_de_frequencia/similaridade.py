from typing import Dict


def score_chi_quadrado(freq_obs: Dict[str, float], freq_esp: Dict[str, float]) -> float:
    """Calcula o score chi-quadrado entre frequências observadas e esperadas.
    
    O chi-quadrado mede a diferença entre a distribuição observada e esperada.
    Valores menores indicam maior similaridade com o perfil esperado.
    
    Args:
        freq_obs: Dicionário com frequências relativas observadas
        freq_esp: Dicionário com frequências relativas esperadas
    
    Returns:
        Score chi-quadrado (quanto menor, melhor o ajuste)
    """

    chi2 = 0.0
    
    for letra in freq_esp:
        observado = freq_obs.get(letra, 0)
        esperado = freq_esp[letra]
        
        if esperado > 0:
            chi2 += ((observado - esperado) ** 2) / esperado
    
    return chi2