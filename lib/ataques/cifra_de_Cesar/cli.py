import argparse
from typing import Optional, Dict

from .cipher import (
    cifrar,
    decifrar,
)


def ler_arquivo_texto(caminho: str) -> str:
    """
    Lê o conteúdo de um arquivo de texto codificado em UTF-8.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)
    except OSError as e:
        print(f"Erro ao abrir o arquivo '{caminho}': {e}")
        sys.exit(1)


def imprimir_resultados(resultados: Dict[str, str]) -> None:
    """Imprime os resultados de forma organizada."""
    print("\n==== RESULTADOS ====")
    for chave, valor in resultados.items():
        print(f"{chave}: {valor}")
    print("====================\n")


def montar_parser() -> argparse.ArgumentParser:
    """
    Cria e configura o analisador de argumentos da CLI.
    """
    parser = argparse.ArgumentParser(
        description="Ferramenta de linha de comando para a Cifra de César."
    )

    parser.add_argument(
        "acao",
        choices=["cifrar", "decifrar"],
        help="Escolha a operação desejada.",
    )

    parser.add_argument(
        "-t", "--texto",
        type=str,
        help="Texto a ser processado."
    )

    parser.add_argument(
        "-f", "--arquivo",
        type=str,
        help="Caminho para arquivo contendo o texto."
    )

    parser.add_argument(
        "-k", "--chave",
        type=int,
        required=True,
        help="Chave da cifra (inteiro)."
    )

    parser.add_argument(
        "--alfabeto",
        type=str,
        default="abcdefghijklmnopqrstuvwxyz",
        help="Alfabeto a ser usado. Padrão: abcdefghijklmnopqrstuvwxyz"
    )

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    """
    Função principal da ferramenta de linha de comando.
    """
    parser = montar_parser()
    args = parser.parse_args(argv)

    if args.texto:
        texto = args.texto
    elif args.arquivo:
        texto = ler_arquivo_texto(args.arquivo)
    else:
        parser.error("É necessário fornecer --texto ou --arquivo.")

    if args.acao == "cifrar":
        processado = cifrar(texto, args.chave, args.alfabeto)
    else:
        processado = decifrar(texto, args.chave, args.alfabeto)

    # Mostra resultados
    imprimir_resultados({
        "Texto original": texto,
        "Texto processado": processado,
        "Chave utilizada": str(args.chave)
    })


if __name__ == "__main__":
    main()