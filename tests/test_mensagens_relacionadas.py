"""
Testes unitários para mensagens_relacionadas.py
Executar com: pytest -v
"""

import sys
import pytest
import os

# adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lib.ataques.rsa_franklin_reiter.mensagens_relacionadas import (
    expandir_relacao_linear,
    construir_polinomio_para_cifra,
    construir_polinomio_de_relacao,
    tentativa_de_recuperacao_de_mensagem
)
from lib.ataques.rsa_franklin_reiter.polynomial import poly_eval


class TestExpandirRelacaoLinear:
    """Testa a função expandir_relacao_linear"""

    def test_expansao_basica_sem_modulo(self):
        """Testa expansão de (x + 1)^2 - 3 = x^2 + 2x + 1 - 3 = x^2 + 2x - 2"""
        # (1*x + 1)^2 - 3
        coefs = expandir_relacao_linear(a=1, b=1, e=2, c=3, n=None)
        # Esperado: [-2, 2, 1] representando -2 + 2x + x^2
        assert coefs == [-2, 2, 1]

    def test_expansao_com_coeficiente_a(self):
        """Testa expansão de (2*x + 1)^2 - 3"""
        # (2*x + 1)^2 - 3 = 4x^2 + 4x + 1 - 3 = 4x^2 + 4x - 2
        coefs = expandir_relacao_linear(a=2, b=1, e=2, c=3, n=None)
        # Esperado: [-2, 4, 4] representando -2 + 4x + 4x^2
        assert coefs == [-2, 4, 4]

    def test_expansao_grau_1(self):
        """Testa expansão de (3*x + 5)^1 - 7"""
        # 3x + 5 - 7 = 3x - 2
        coefs = expandir_relacao_linear(a=3, b=5, e=1, c=7, n=None)
        # Esperado: [-2, 3] representando -2 + 3x
        assert coefs == [-2, 3]

    def test_expansao_com_modulo(self):
        """Testa expansão com redução modular"""
        # (2*x + 1)^2 - 3 mod 5 = 4x^2 + 4x - 2 mod 5 = 4x^2 + 4x + 3 mod 5
        coefs = expandir_relacao_linear(a=2, b=1, e=2, c=3, n=5)
        # -2 mod 5 = 3
        assert coefs == [3, 4, 4]

    def test_expansao_grau_3_sem_modulo(self):
        """Testa expansão de (x + 2)^3 - 5"""
        # (x + 2)^3 = x^3 + 3*x^2*2 + 3*x*4 + 8 = x^3 + 6x^2 + 12x + 8
        # Subtraindo 5: x^3 + 6x^2 + 12x + 3
        coefs = expandir_relacao_linear(a=1, b=2, e=3, c=5, n=None)
        assert coefs == [3, 12, 6, 1]

    def test_expansao_grau_zero(self):
        """Testa expansão de (x)^0 - 1 = 1 - 1 = 0"""
        coefs = expandir_relacao_linear(a=1, b=0, e=0, c=1, n=None)
        assert coefs == [0]


class TestConstruirPolinomioParaCifra:
    """Testa construir_polinomio_para_cifra"""

    def test_f_basico(self):
        """Testa construção de f(x) = x^2 - 5"""
        f_coefs, _ = construir_polinomio_para_cifra(e=2, c1=5, a=1, b=0, c2=0)
        # f(x) = x^2 - 5
        assert f_coefs == [-5, 0, 1]

    def test_g_basico(self):
        """Testa construção de g(x) = (x + 1)^2 - 10"""
        _, g_coefs = construir_polinomio_para_cifra(e=2, c1=5, a=1, b=1, c2=10)
        # (x + 1)^2 - 10 = x^2 + 2x + 1 - 10 = x^2 + 2x - 9
        assert g_coefs == [-9, 2, 1]

    def test_ambos_polinomios(self):
        """Testa construção de ambos os polinômios"""
        e = 3
        c1 = 7
        a = 2
        b = 3
        c2 = 11
        
        f_coefs, g_coefs = construir_polinomio_para_cifra(e, c1, a, b, c2)
        
        # f(x) = x^3 - 7
        assert f_coefs == [-7, 0, 0, 1]
        assert len(f_coefs) == 4
        
        # g(x) = (2x + 3)^3 - 11
        # (2x + 3)^3 = 8x^3 + 36x^2 + 54x + 27
        assert g_coefs == [27 - 11, 54, 36, 8]
        assert g_coefs == [16, 54, 36, 8]
        assert len(g_coefs) == 4

    def test_e_negativo_lanca_erro(self):
        """Testa que e negativo lança ValueError"""
        with pytest.raises(ValueError):
            construir_polinomio_para_cifra(e=-1, c1=5, a=1, b=0, c2=0)

    def test_e_nao_inteiro_lanca_erro(self):
        """Testa que e não-inteiro lança ValueError"""
        with pytest.raises(ValueError):
            construir_polinomio_para_cifra(e=2.5, c1=5, a=1, b=0, c2=0)

    def test_tamanho_polinomios(self):
        """Testa que ambos polinômios têm tamanho e+1"""
        e = 5
        f_coefs, g_coefs = construir_polinomio_para_cifra(e, 10, 2, 3, 15)
        assert len(f_coefs) == e + 1
        assert len(g_coefs) == e + 1


class TestConstruirPolinomioDeRelacao:
    """Testa construir_polinomio_de_relacao"""

    def test_polinomio_sem_modulo_n_grande(self):
        """Testa com n muito grande (efetivamente sem modulo)"""
        n = 2**256
        coefs = construir_polinomio_de_relacao(a=1, b=1, e=2, c=3, n=n)
        # Com n grande, -2 mod n = n-2
        assert coefs == [(n - 2) % n, 2, 1]
        assert coefs[1] == 2
        assert coefs[2] == 1

    def test_polinomio_com_modulo_pequeno(self):
        """Testa com modulo pequeno"""
        # (2*x + 1)^2 - 3 mod 5
        coefs = construir_polinomio_de_relacao(a=2, b=1, e=2, c=3, n=5)
        assert coefs == [3, 4, 4]  # -2 ≡ 3 (mod 5)

    def test_polinomio_grau_3_com_modulo(self):
        """Testa polinômio de grau 3 com módulo"""
        n = 11
        # (2*x + 1)^3 - 5 mod 11
        coefs = construir_polinomio_de_relacao(a=2, b=1, e=3, c=5, n=n)
        
        # Cálculo manual: (2x+1)^3 = 8x^3 + 12x^2 + 6x + 1
        # - 5 = 8x^3 + 12x^2 + 6x - 4
        # mod 11: 8x^3 + x^2 + 6x + 7
        assert len(coefs) == 4
        assert all(0 <= c < n for c in coefs)

    def test_relacao_linear_com_a_grande(self):
        """Testa com a > 1"""
        n = 23
        coefs = construir_polinomio_de_relacao(a=5, b=3, e=2, c=10, n=n)
        
        # (5x + 3)^2 - 10 = 25x^2 + 30x + 9 - 10 = 25x^2 + 30x - 1
        # coef k: comb(2,k) * 5^k * 3^(2-k) - c
        # k=0: 1 * 1 * 9 - 10 = -1 mod 23 = 22
        # k=1: 2 * 5 * 3 = 30 mod 23 = 7
        # k=2: 1 * 25 * 1 = 25 mod 23 = 2
        assert len(coefs) == 3
        assert coefs[0] == 22  # -1 mod 23
        assert coefs[1] == 7   # 30 mod 23
        assert coefs[2] == 2   # 25 mod 23


class TestTentativaDeRecuperacaoDeMensagem:
    """Testa tentativa_de_recuperacao_de_mensagem"""

    def test_raiz_encontrada_simples(self):
        """Testa quando a raiz é encontrada (x - 2)"""
        # Polinômio: x - 2, tem raiz em x = 2
        # Coeficientes: [-2, 1]
        polinomio = [-2, 1]
        n = 10
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        assert resultado == 2

    def test_raiz_encontrada_quadratico(self):
        """Testa raiz de polinômio quadrático"""
        # (x - 3)(x - 5) = x^2 - 8x + 15
        # Coeficientes: [15, -8, 1]
        polinomio = [15, -8, 1]
        n = 20
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        # deve encontrar 3 ou 5
        assert resultado in [3, 5]

    def test_raiz_nao_encontrada(self):
        """Testa quando não há raiz no intervalo"""
        polinomio = [1, 0, 1]  # x^2 + 1
        n = 7
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        # x^2 + 1 mod 7 não tem raízes em [0, 6]
        assert resultado is None

    def test_raiz_em_zero(self):
        """Testa quando a raiz é 0"""
        # Polinômio com raiz em 0: x
        # Coeficientes: [0, 1]
        polinomio = [0, 1]
        n = 10
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        assert resultado == 0

    def test_polinomio_zero(self):
        """Testa polinômio identicamente zero"""
        polinomio = [0]
        n = 10
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        assert resultado == 0  # qualquer x é raiz, retorna o primeiro

    def test_raiz_modular(self):
        """Testa busca de raiz modular"""
        # (x - 3) mod 7 = x - 3 (mod 7)
        # raiz em x = 3
        polinomio = [-3, 1]
        n = 7
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        assert resultado == 3

    def test_performance_intervalo_grande(self):
        """Testa com intervalo maior (pode ser lento)"""
        # busca linear, então pode ser lenta com n grande
        # x - 50, raiz em x = 50
        polinomio = [-50, 1]
        n = 100
        
        resultado = tentativa_de_recuperacao_de_mensagem(polinomio, n)
        assert resultado == 50


class TestIntegracaoFranklinReiter:
    """Testes de integração do ataque Franklin-Reiter"""

    def test_caso_pequeno_franklin_reiter(self):
        """Testa um caso pequeno de Franklin-Reiter"""
        # RSA simples: n = 33, e = 3
        # m1 = 5, m2 = 8 (relação: m2 = 1*m1 + 3)
        e = 3
        n = 33
        m1 = 5
        a = 1
        b = 3
        
        c1 = pow(m1, e, n)  # 5^3 mod 33 = 125 mod 33 = 26
        m2 = (a * m1 + b) % n
        c2 = pow(m2, e, n)  # 8^3 mod 33 = 512 mod 33 = 14
        
        # Construir polinômios
        f_coefs, g_coefs = construir_polinomio_para_cifra(e, c1, a, b, c2)
        
        # Verificar que f(m1) = 0 (mod n) e g(m1) = 0 (mod n)
        assert poly_eval(f_coefs, m1) % n == 0
        assert poly_eval(g_coefs, m1) % n == 0

    def test_coeficientes_consistentes(self):
        """Testa que construir_polinomio_para_cifra e construir_polinomio_de_relacao
        são consistentes para g(x)"""
        a, b, e = 2, 3, 4
        c2 = 100
        n = 2**20  # n grande
        
        _, g_coefs_1 = construir_polinomio_para_cifra(e, 50, a, b, c2)
        g_coefs_2 = construir_polinomio_de_relacao(a, b, e, c2, n)
        
        # deve ser o mesmo resultado depois de redução modular
        assert [c % n for c in g_coefs_1] == g_coefs_2