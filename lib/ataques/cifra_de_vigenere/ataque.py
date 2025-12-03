from lib.ataques.cifra_de_vigenere.vigenere import VigenereCifra


def atacar(texto_cifrado):
    vigenere = VigenereCifra()
    tamanho_chave = vigenere.tamanho_chave(texto_cifrado, verbose = False)
    chave = vigenere.quebra_chave(texto_cifrado, tamanho_chave)
    return vigenere.encriptar_decriptar(texto_cifrado,chave,"decifrar")