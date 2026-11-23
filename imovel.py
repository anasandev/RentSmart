"""Classes e regras compartilhadas pelos tipos de imovel."""

from decimal import Decimal


CENTAVO = Decimal("0.01")


class Imovel:
    """Representa os valores comuns a qualquer imovel oferecido para locacao."""

    def __init__(
        self,
        tipo: str,
        valor_base: Decimal,
        adicionais: tuple[tuple[str, Decimal], ...] = (),
    ) -> None:
        self._tipo = tipo
        self._valor_base = valor_base
        self._adicionais = adicionais

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def valor_base(self) -> Decimal:
        return self._valor_base

    @property
    def adicionais(self) -> tuple[tuple[str, Decimal], ...]:
        return self._adicionais

    @property
    def valor_adicionais(self) -> Decimal:
        return sum((valor for _, valor in self._adicionais), Decimal("0.00"))

    @property
    def valor_bruto(self) -> Decimal:
        return self._valor_base + self.valor_adicionais

    @property
    def valor_desconto(self) -> Decimal:
        return Decimal("0.00")

    @property
    def valor_aluguel(self) -> Decimal:
        return (self.valor_bruto - self.valor_desconto).quantize(CENTAVO)

    def detalhes(self) -> tuple[str, ...]:
        """Retorna informacoes especificas do imovel para o resumo."""
        return ()
