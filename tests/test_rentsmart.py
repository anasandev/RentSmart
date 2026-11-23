"""Testes das regras comerciais e da projecao CSV do RentSmart."""

import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from apartamento import Apartamento
from casa import Casa
from orcamento import Orcamento
from projecao import ProjecaoCSV
from studio import Studio


class TestRentSmart(unittest.TestCase):
    def test_apartamento_com_garagem_e_sem_criancas(self) -> None:
        apartamento = Apartamento(1, True, False)
        orcamento = Orcamento(apartamento, 4)

        self.assertEqual(apartamento.valor_adicionais, Decimal("300.00"))
        self.assertEqual(apartamento.valor_desconto, Decimal("50.00"))
        self.assertEqual(apartamento.valor_aluguel, Decimal("950.00"))
        self.assertEqual(orcamento.total_primeiro_mes, Decimal("1450.00"))

    def test_casa_de_dois_quartos_com_garagem(self) -> None:
        casa = Casa(2, True)

        self.assertEqual(casa.valor_adicionais, Decimal("550.00"))
        self.assertEqual(casa.valor_desconto, Decimal("0.00"))
        self.assertEqual(casa.valor_aluguel, Decimal("1450.00"))

    def test_estudio_com_tres_vagas(self) -> None:
        estudio = Studio(3)

        self.assertEqual(estudio.valor_adicionais, Decimal("310.00"))
        self.assertEqual(estudio.valor_aluguel, Decimal("1510.00"))

    def test_estudio_sem_estacionamento(self) -> None:
        estudio = Studio(0)

        self.assertEqual(estudio.valor_adicionais, Decimal("0.00"))
        self.assertEqual(estudio.valor_aluguel, Decimal("1200.00"))

    def test_parcelas_somam_a_taxa_e_sao_distribuidas_em_centavos(self) -> None:
        for quantidade in (1, 2, 3, 4, 5):
            with self.subTest(quantidade=quantidade):
                orcamento = Orcamento(Casa(1, False), quantidade)

                self.assertEqual(len(orcamento.parcelas), quantidade)
                self.assertEqual(sum(orcamento.parcelas), Decimal("2000.00"))
                self.assertEqual(orcamento.valor_taxa, Decimal("2000.00"))

    def test_taxa_separada_e_distribuida_no_csv(self) -> None:
        orcamento = Orcamento(Apartamento(1, True, False), 3)
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = ProjecaoCSV(orcamento).gerar(
                Path(diretorio) / "projecao.csv"
            )
            with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
                linhas = list(csv.DictReader(arquivo))

        self.assertEqual(len(linhas), 12)
        self.assertEqual(
            list(linhas[0].keys()),
            [
                "Mês",
                "Aluguel mensal",
                "Parcela contratual",
                "Total mensal previsto",
            ],
        )
        self.assertEqual(
            [linha["Parcela contratual"] for linha in linhas[:3]],
            ["666.67", "666.67", "666.66"],
        )
        self.assertTrue(
            all(linha["Parcela contratual"] == "0.00" for linha in linhas[3:])
        )
        self.assertTrue(all(linha["Aluguel mensal"] == "950.00" for linha in linhas))

    def test_rejeita_quartos_e_parcelas_invalidos(self) -> None:
        with self.assertRaises(ValueError):
            Apartamento(3, False, False)
        with self.assertRaises(ValueError):
            Casa(0, False)
        with self.assertRaises(ValueError):
            Orcamento(Studio(0), 6)
        with self.assertRaises(ValueError):
            Studio(1)


if __name__ == "__main__":
    unittest.main()
