"""Calculos do aluguel e da taxa contratual."""

from decimal import Decimal

from imovel import CENTAVO, Imovel


class Orcamento:
    """Reune os dados do imovel e calcula os valores do contrato."""

    def __init__(self, imovel: Imovel, quantidade_parcelas: int) -> None:
        if quantidade_parcelas not in range(1, 6):
            raise ValueError("A taxa contratual pode ser parcelada de 1 a 5 vezes.")

        self._imovel = imovel
        self._quantidade_parcelas = quantidade_parcelas
        self._valor_taxa = Decimal("2000.00")
        self._parcelas = self._calcular_parcelas()

    @property
    def imovel(self) -> Imovel:
        return self._imovel

    @property
    def quantidade_parcelas(self) -> int:
        return self._quantidade_parcelas

    @property
    def valor_taxa(self) -> Decimal:
        return self._valor_taxa

    @property
    def parcelas(self) -> tuple[Decimal, ...]:
        return self._parcelas

    @property
    def total_primeiro_mes(self) -> Decimal:
        return self._imovel.valor_aluguel + self._parcelas[0]

    def _calcular_parcelas(self) -> tuple[Decimal, ...]:
        total_centavos = int(self._valor_taxa * 100)
        valor_base, centavos_restantes = divmod(
            total_centavos, self._quantidade_parcelas
        )
        return tuple(
            (
                Decimal(valor_base + (1 if indice < centavos_restantes else 0))
                / Decimal("100")
            ).quantize(CENTAVO)
            for indice in range(self._quantidade_parcelas)
        )

    def resumo(self) -> str:
        imovel = self._imovel
        linhas = [
            "=== Orçamento de locação - R.M Imóveis ===",
            f"Tipo de imóvel: {imovel.tipo}",
            *imovel.detalhes(),
            "Adicionais contratados:",
        ]
        if imovel.adicionais:
            linhas.extend(
                f"  - {descricao}: {self._formatar_moeda(valor)}"
                for descricao, valor in imovel.adicionais
            )
        else:
            linhas.append("  - Nenhum")
        linhas.extend(
            [
                f"Valor dos adicionais: {self._formatar_moeda(imovel.valor_adicionais)}",
                f"Desconto aplicado: {self._formatar_moeda(imovel.valor_desconto)}",
                f"Aluguel mensal final: {self._formatar_moeda(imovel.valor_aluguel)}",
                f"Taxa contratual total: {self._formatar_moeda(self._valor_taxa)}",
                f"Quantidade de parcelas: {self._quantidade_parcelas}",
                "Valor das parcelas: "
                + ", ".join(self._formatar_moeda(valor) for valor in self._parcelas),
                f"Total a pagar no primeiro mês: {self._formatar_moeda(self.total_primeiro_mes)}",
            ]
        )
        return "\n".join(linhas)

    @staticmethod
    def _formatar_moeda(valor: Decimal) -> str:
        valor_formatado = f"{valor:,.2f}"
        valor_formatado = valor_formatado.replace(",", "X")
        valor_formatado = valor_formatado.replace(".", ",")
        valor_formatado = valor_formatado.replace("X", ".")
        return f"R$ {valor_formatado}"
