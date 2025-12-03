from typing import Dict, Callable, List
import time 
from .texto import indice_coincidencia
from .algoritmos import medir_tempo, expansao_tamanho, calcular_avalanche

def comparar_algoritmos(textos: Dict[str, str], algoritmos: Dict[str, Dict[str, Callable]]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Compara tempo de cifragem/decifragem e métricas de criptoanálise para vários algoritmos e textos.
    """
    resultados = {}

    for nome_alg, funcs in algoritmos.items():
        resultados[nome_alg] = {}
        func_cifrar = funcs["cifrar"]
        func_decifrar = funcs["decifrar"]
        
        for nome_txt, texto in textos.items():
            
            start_time_cifra = time.perf_counter()
            cifrado = func_cifrar(texto) 
            tempo_cifra = time.perf_counter() - start_time_cifra
            tempo_decifra = medir_tempo(func_decifrar, cifrado)
            tamanho_bytes = len(texto.encode('utf-8'))
            
            resultados[nome_alg][nome_txt] = {
                "tamanho": tamanho_bytes,
                "tempo_cifra": tempo_cifra,
                "tempo_decifra": tempo_decifra,
                "IC": indice_coincidencia(cifrado),
                "expansao": expansao_tamanho(texto, cifrado),
                "avalanche": calcular_avalanche(func_cifrar, texto),
            }

    return resultados