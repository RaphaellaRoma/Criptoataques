from typing import Dict, Callable, List
import time 
from .texto import indice_coincidencia, entropia, gerar_dados_cripto_graficos
from .algoritmos import medir_tempo, expansao_tamanho, calcular_avalanche


def comparar_algoritmos(textos: Dict[str, str], algoritmos: Dict[str, Dict[str, Callable]], max_shift_auto: int = 50):
    """
    Compara tempo de cifragem/decifragem e métricas de criptoanálise para vários algoritmos e textos.
    """
    resultados = {}

    for nome_alg, funcs in algoritmos.items():
        resultados[nome_alg] = {}

        for nome_txt, texto in textos.items():

            # tempo
            start = time.perf_counter()
            cifrado = funcs["cifrar"](texto)
            tempo_cifra = time.perf_counter() - start

            tempo_decifra = medir_tempo(funcs["decifrar"], cifrado)
            tempo_ataque = medir_tempo(funcs["atacar"], cifrado)

            tamanho_bytes = len(texto.encode('utf-8'))

            # numeros matriz
            dados_graf = gerar_dados_cripto_graficos(texto, funcs["cifrar"], max_shift_auto)

            resultados[nome_alg][nome_txt] = {
                "tamanho": tamanho_bytes,
                "tempo_cifra": tempo_cifra,
                "tempo_decifra": tempo_decifra,
                "tempo_ataque": tempo_ataque,

                "IC": indice_coincidencia(cifrado),
                "expansao": expansao_tamanho(len(texto), len(cifrado)),
                "avalanche": calcular_avalanche(funcs["cifrar"], texto),
                "entropia": entropia(cifrado),
                "autocorrelacao": dados_graf["autocorrelacao"],
                "coocorrencia": dados_graf["coocorrencia"],
            }

    return resultados