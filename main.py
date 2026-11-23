"""Ponto de entrada da aplicacao RentSmart."""

from pathlib import Path

from apartamento import Apartamento
from casa import Casa
from imovel import Imovel
from orcamento import Orcamento
from projecao import ProjecaoCSV
from studio import Studio


def ler_inteiro(mensagem: str, opcoes: tuple[int, ...] | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue

        if opcoes is not None and valor not in opcoes:
            print(f"Opção inválida. Escolha entre: {', '.join(map(str, opcoes))}.")
            continue
        return valor


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida. Digite S para sim ou N para não.")


def escolher_imovel() -> Imovel | None:
    print("\n=== RentSmart | R.M Imóveis ===")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    print("0 - Sair")

    escolha = ler_inteiro("Escolha o tipo de imóvel: ", (0, 1, 2, 3))
    if escolha == 0:
        return None

    if escolha == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", (1, 2))
        garagem = ler_sim_nao("Deseja contratar garagem por R$ 300,00? (S/N): ")
        criancas = ler_sim_nao("Possui crianças? (S/N): ")
        return Apartamento(quartos, garagem, criancas)

    if escolha == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", (1, 2))
        garagem = ler_sim_nao("Deseja contratar garagem por R$ 300,00? (S/N): ")
        return Casa(quartos, garagem)

    vagas = ler_inteiro(
        "Quantidade de vagas (0 para nenhuma ou 2 ou mais): "
    )
    while vagas != 0 and vagas < 2:
        print("Opção inválida. Escolha 0 ou pelo menos 2 vagas.")
        vagas = ler_inteiro(
            "Quantidade de vagas (0 para nenhuma ou 2 ou mais): "
        )
    return Studio(vagas)


def main() -> None:
    imovel = escolher_imovel()
    if imovel is None:
        print("Programa encerrado.")
        return

    parcelas = ler_inteiro(
        "Quantidade de parcelas da taxa contratual (1 a 5): ",
        (1, 2, 3, 4, 5),
    )
    orcamento = Orcamento(imovel, parcelas)

    print()
    print(orcamento.resumo())

    caminho_csv = Path(__file__).resolve().parent / "resultados" / "projecao_rentsmart.csv"
    caminho_salvo = ProjecaoCSV(orcamento).gerar(caminho_csv)
    print(f"\nProjecao CSV salva em: {caminho_salvo}")


if __name__ == "__main__":
    main()
