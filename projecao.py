"""Gera a projecao financeira do contrato em arquivo CSV."""

import csv
from pathlib import Path
from decimal import Decimal

from orcamento import Orcamento


class ProjecaoCSV:
    """Escreve os doze meses de aluguel e parcelas contratuais."""

    CABECALHO = (
        "Mês",
        "Aluguel mensal",
        "Parcela contratual",
        "Total mensal previsto",
    )

    def __init__(self, orcamento: Orcamento) -> None:
        self._orcamento = orcamento

    def gerar(self, caminho: Path) -> Path:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(self.CABECALHO)
            for mes in range(1, 13):
                parcela = (
                    self._orcamento.parcelas[mes - 1]
                    if mes <= self._orcamento.quantidade_parcelas
                    else Decimal("0.00")
                )
                aluguel = self._orcamento.imovel.valor_aluguel
                escritor.writerow(
                    (
                        mes,
                        f"{aluguel:.2f}",
                        f"{parcela:.2f}",
                        f"{aluguel + parcela:.2f}",
                    )
                )
        return caminho
