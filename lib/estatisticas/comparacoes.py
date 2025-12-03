"""
Ferramentas para comparar vários algoritmos em vários textos.
"""

from typing import Dict, Callable, List
from .texto import indice_coincidencia
from .algoritmos import medir_tempo, expansao_tamanho, calcular_avalanche


def comparar_algoritmos(textos: Dict[str, str], algoritmos: Dict[str, Dict[str, Callable]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Compara tempo de cifragem/decifragem e métricas de criptoanálise para vários algoritmos e textos.
    A entrada 'algoritmos' deve ter a estrutura: {NomeAlg: {"cifrar": func_c, "decifrar": func_d}}
    """
    resultados = {}

    for nome_alg, funcs in algoritmos.items():
        resultados[nome_alg] = {}
        func_cifrar = funcs["cifrar"]
        func_decifrar = funcs["decifrar"]
        
        for nome_txt, texto in textos.items():
            cifrado = func_cifrar(texto)
            tamanho_bytes = len(texto.encode('utf-8'))
            
            resultados[nome_alg][nome_txt] = {
                "tamanho": tamanho_bytes,
                "tempo_cifra": medir_tempo(func_cifrar, texto, repeticoes=5),
                "tempo_decifra": medir_tempo(func_decifrar, cifrado, repeticoes=5),
                "IC": indice_coincidencia(cifrado),
                "expansao": expansao_tamanho(texto, cifrado),
                "avalanche": calcular_avalanche(func_cifrar, texto),
            }

    return resultados