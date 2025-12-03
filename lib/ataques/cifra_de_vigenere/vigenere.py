import string as s
from itertools import combinations
import unicodedata
import re

class VigenereCifra:
    def __init__(self):
        self._alfabeto = list(s.ascii_uppercase)
        self._freq_pt = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]
        self._freq_ing =[8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    
    # Funções auxiliares
    def _normalizar_texto_para_cifrar(self, texto: str) -> str:
        # remove acentos (Ç→C, Á→A...)
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        return texto.upper()
    
    def _limpar_texto(self, texto: str) -> str:
        """Remove caracteres não alfabéticos e converte para maiúsculas."""
        
        # Normaliza acentos (É → E, Ç → C, Ã → A...)
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')

        # Agora deixa só A–Z
        texto = texto.upper()
        texto = re.sub(r'[^A-Z]', '', texto)

        return texto
    
    def _descobrir_letra(self, probabilidades, idioma):
        melhor_letra = ''
        menor_diferenca = float('inf')

        if idioma == 'EN':
            freq_idioma = self._freq_ing
        else:
            freq_idioma = self._freq_pt

        for shift in range(26):
            soma_diferencas = 0

            # Compara a distribuição rotacionada com a frequência do idioma
            for j in range(26):
                soma_diferencas += abs(probabilidades[(shift + j) % 26] - freq_idioma[j])

            # Escolhe o shift com menor diferença
            if soma_diferencas < menor_diferenca:
                menor_diferenca = soma_diferencas
                melhor_letra = self._alfabeto[shift]

        return melhor_letra


    def _transformar_chave(self, texto: str, chave: str) -> str:
        chave = self._limpar_texto(chave).upper()

        nova = ""
        i = 0

        for c in texto:
            if c in self._alfabeto:
                nova += chave[i]
                i = (i + 1) % len(chave)
            else:
                nova += c  # mantém espaço/pontuação/algo não-AZ
        return nova




    # FUNÇÕES PRINCIPAIS
    def tamanho_chave(self, texto_cifrado: str, max_key_length: int = 20, verbose=True) -> int:
        """Estima o tamanho da chave usando o método de Kasiski."""
        texto = self._limpar_texto(texto_cifrado)

        pos_trigramas = {}
        for i in range(1, len(texto)-2):
            trigrama = texto[i:i+3]
            pos_trigramas.setdefault(trigrama, []).append(i)
        distancias = {}
        # calcula distâncias entre ocorrências de trigramas
        for trigrama, posicoes in pos_trigramas.items():
            if len(posicoes) > 1:
                for i in range(len(posicoes)-1):
                    for p1, p2 in combinations(posicoes, 2):
                        distancia = p2 - p1
                        distancias.setdefault(trigrama, []).append(distancia)
        
        distancias_completo = set()
        for dist in distancias.values():
            distancias_completo.update(dist)
        distancias_completo = list(distancias_completo)
        
        freq_divisores = {i: 0 for i in range(4, max_key_length + 1)}

        for dist in distancias_completo:
            for div in range(4, max_key_length + 1):
                if dist % div == 0:
                    freq_divisores[div] += 1

        freq_divisores_sorted = dict(sorted(freq_divisores.items(), key=lambda x: x[1], reverse=True))
        if verbose:
            print("Tamanhos de chave possíveis (ordenados por frequência):")
            for tamanho, qtd in freq_divisores_sorted.items():
                print(f"Tamanho: {tamanho} -- Quantidade: {qtd}")

            tamanho_provavel = next(iter(freq_divisores_sorted))

            print("\nTamanho provável da chave:", tamanho_provavel)

        # Perguntar ao usuário
        # ans = input("Você deseja continuar com esse tamanho da chave? (S/N)\n>>> ")

        # if ans.lower() == 'n':
        #     escolha = int(input(f"Digite o tamanho da chave desejado (entre 4 e {max_key_length}).\n>>> "))
        #     while escolha < 4 or escolha > max_key_length:
        #         escolha = int(input(f"Tamanho inválido. Digite um número entre 4 e {max_key_length}.\n>>> "))
        #     return escolha

        return next(iter(freq_divisores_sorted))


    def quebra_chave(self, texto_cifrado: str, tamanho_chave: int, idioma: str = 'pt') -> str:
        """Quebra a cifra de Vigenère dado o tamanho da chave."""
        texto = self._limpar_texto(texto_cifrado)
        palavra_chave = ""

        for indice in range(tamanho_chave):

            # Frequência das letras dessa coluna
            freq_coluna = {}
            total = 0

            for pos in range(indice, len(texto), tamanho_chave):
                letra = texto[pos]
                freq_coluna[letra] = freq_coluna.get(letra, 0) + 1
                total += 1

            # Constrói vetor de probabilidades na ordem do alfabeto
            probabilidades = [
                (freq_coluna.get(letra, 0) / total) * 100
                for letra in self._alfabeto
            ]

            # Descobre letra da chave
            letra_chave = self._descobrir_letra(probabilidades, idioma)
            palavra_chave += letra_chave

        return palavra_chave


    # def encriptar_decriptar(self, texto: str, chave: str, opcao: str) -> str:
    #     """Encripta ou decripta o texto usando a cifra de Vigenère."""
    #     if opcao in ('ENCRIPTAR', 'DECRIPTAR'):
    #         if len(texto) <= 0 or len(chave) < 3:
    #             raise ValueError('Tamanho do texto ou da chave inválido')
    #     else:
    #         raise ValueError('Opção inválida!')

    #     if opcao != 'ENCRIPTAR' and opcao != 'DECRIPTAR':
    #         raise ValueError('Opção inválida!')
    #     texto = self._limpar_texto(texto)
    #     chave = self._limpar_texto(chave)
    #     chave_nova = self._transformar_chave(texto, chave)

    #     resultado = ""
    #     for letra in texto:
    #         if opcao == 'ENCRIPTAR':
    #             nova_letra = self._alfabeto[(self._alfabeto.index(letra) + self._alfabeto.index(chave_nova[len(resultado)])) % 26]
    #         else:
    #             nova_letra = self._alfabeto[(self._alfabeto.index(letra) - self._alfabeto.index(chave_nova[len(resultado)]) + 26) % 26]
    #         resultado += nova_letra

    #     return resultado
    
    def encriptar_decriptar(self, texto: str, chave: str, opcao: str) -> str:
        if opcao not in ('cifrar', 'decifrar'):
            raise ValueError('Opção inválida!')

        if len(texto) <= 0 or len(chave) < 4:
            raise ValueError('Tamanho do texto ou da chave inválido')

        # texto com espaços preservados e acentos removidos
        texto_norm = self._normalizar_texto_para_cifrar(texto)
        
        # gera chave alinhada ao texto completo
        chave_norm = self._limpar_texto(chave)
        chave_nova = self._transformar_chave(texto_norm, chave_norm)

        resultado = ""
        for letra, k in zip(texto_norm, chave_nova):
            if letra in self._alfabeto:
                pos_letra = self._alfabeto.index(letra)
                pos_chave = self._alfabeto.index(k)

                if opcao == 'cifrar':
                    nova = self._alfabeto[(pos_letra + pos_chave) % 26]
                else:
                    nova = self._alfabeto[(pos_letra - pos_chave + 26) % 26]

                resultado += nova
            else:
                resultado += letra  # copia o símbolo intacto

        return resultado