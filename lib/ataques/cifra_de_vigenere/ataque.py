from lib.ataques.cifra_de_vigenere.vigenere import VigenereCifra


def atacar(texto_cifrado):
    """
    Ataca automaticamente a cifra de Vigenère:
    1. Estima o tamanho da chave.
    2. Recupera a chave por análise de frequência.
    3. Decifra o texto.
    Retorna o texto decifrado.
    """
    vigenere = VigenereCifra()
    tamanho_chave = vigenere.tamanho_chave(texto_cifrado, verbose = False)
    chave = vigenere.quebra_chave(texto_cifrado, tamanho_chave)
    return vigenere.encriptar_decriptar(texto_cifrado,chave,"decifrar")