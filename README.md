# Criptoataques

Este projeto reúne implementações de algoritmos clássicos de criptografia, métodos de cifragem/decifragem e estudos de criptoanálise prática, com foco especial em:

- Estudos históricos de criptografia (Cesar e Vigenère)
- Criptografia RSA (Frenklin Reiter)
- Análise de frequência   
- Comparação entre algoritmos  

<br>

---

<br>

# Objetivo Acadêmico

O objetivo deste trabalho é compreender não apenas a matemática dos algoritmos, mas também como explorá-los através de ataques reais, tentamos:

- Explicar o fundamento matemático dos ataques.

- Mostrar como cifras clássicas podem ser quebradas usando estatística.

- Reproduzir técnicas de criptoanálise usadas, por exemplo, por Al-Kindi, Babbage e Shannon.

- Aplicar o algoritmo RSA () e compará-lo com os algoritmos mais antigos de criptografia.

<br>

---

<br>

# Estrutura do Projeto

```text
.
├── README.md
├── criptoataques.ipynb
├── crypto_io
│   ├── __init__.py
│   ├── normalizador.py
│   └── util_io.py
├── examples
│   └── textos_base
│       ├── Inverno_brasileiro.txt
│       ├── a_assembleia_dos_ratos.txt
│       ├── a_cancao_do_africano.txt
│       ├── a_capital_federal.txt
│       ├── a_semana.txt
│       ├── cancao_do_exilio.txt
│       ├── conto_macabro.txt
│       ├── frankenstein.txt
│       ├── lingua_do_p.txt
│       ├── memorias_postumas_b_c.txt
│       ├── modinha.txt
│       ├── o_homem_e_o_cavalo.txt
│       ├── o_livro_e_a_leitura.txt
│       ├── os_sertoes.txt
│       ├── profissao_de_fe.txt
│       ├── quincas_borba.txt
│       ├── t_f_policarpo_quaresma.txt
│       ├── versos_intimos.txt
│       ├── viagens_na_minha_terra.txt
│       └── vidas_secas.txt
├── lib
│   ├── ataques
│   │   ├── analise_de_frequencia
│   │   │   ├── __init__.py
│   │   │   ├── perfis_linguisticos.py
│   │   │   ├── similaridade.py
│   │   │   └── util_frequencia.py
│   │   ├── cifra_de_Cesar
│   │   │   ├── __init__.py
│   │   │   ├── ataque.py
│   │   │   ├── cipher.py
│   │   │   └── cli.py
│   │   ├── cifra_de_vigenere
│   │   │   ├── ataque.py
│   │   │   └── vigenere.py
│   │   └── rsa_franklin_reiter
│   │       ├── __init__.py
│   │       ├── aritmetica_modular.py
│   │       ├── ataque.py
│   │       ├── gerador_casos.py
│   │       ├── mensagens_relacionadas.py
│   │       ├── polynomial.py
│   │       └── util_rsa.py
│   └── estatisticas
│       ├── __init__.py
│       ├── algoritmos.py
│       ├── comparacoes.py
│       └── texto.py
└── tests
    ├── test_analise_de_frequencia.py
    ├── test_cipher.py
    ├── test_gerador_casos.py
    ├── test_mensagens_relacionadas.py
    ├── test_normalizador.py
    ├── test_polynomial.py
    └── test_util_io.py

```

<br>

---

<br>

# Como Executar


Para executar este projeto, siga os passos abaixo:

1.  **Clonar o Repositório:** 

Abra seu terminal e clone o projeto:

```bash
git clone [https://github.com/RaphaellaRoma/Criptoataques.git](https://github.com/RaphaellaRoma/Criptoataques.git)
cd Criptoataques
````

2.  **Instalar Dependências**

Este projeto requer Python, Jupyter Notebook e bibliotecas científicas como NumPy e Matplotlib.

-   **Crie e Ative um Ambiente Virtual (Recomendado):**

  ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # ou
    .\venv\Scripts\activate   # No Windows (PowerShell/CMD)
  ```

  - **Instale as Bibliotecas Necessárias:**

  ```bash
    pip install numpy matplotlib pandas jupyter
  ```

3.  **Executar as Células:** Prossiga executando as células do notebook sequencialmente. Certifique-se de que cada célula seja executada com sucesso antes de passar para a próxima. 

<br>

---

<br>

# Autores

Projeto desenvolvido como parte do estudo de: **Criptoanálise e Sistemas Clássicos de Criptografia**

Implementações, ataques e documentação por:

*Eliane Moreira*

*Raphaella Roma*

*Stephany Casali*