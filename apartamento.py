"""Regra de calculo para apartamentos."""

from decimal import Decimal, ROUND_HALF_UP

from imovel import CENTAVO, Imovel


class Apartamento(Imovel):
    """Apartamento de um ou dois quartos, com garagem opcional."""

    def __init__(self, quartos: int, possui_garagem: bool, possui_criancas: bool) -> None:
        if quartos not in (1, 2):
            raise ValueError("O apartamento deve ter 1 ou 2 quartos.")

        adicionais: list[tuple[str, Decimal]] = []
        if quartos == 2:
            adicionais.append(("Adicional de 2 quartos", Decimal("200.00")))
        if possui_garagem:
            adicionais.append(("Garagem", Decimal("300.00")))

        super().__init__("Apartamento", Decimal("700.00"), tuple(adicionais))
        self._quartos = quartos
        self._possui_garagem = possui_garagem
        self._possui_criancas = possui_criancas

    @property
    def quartos(self) -> int:
        return self._quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    @property
    def possui_criancas(self) -> bool:
        return self._possui_criancas

    @property
    def valor_desconto(self) -> Decimal:
        if self._possui_criancas:
            return Decimal("0.00")
        return (self.valor_bruto * Decimal("0.05")).quantize(
            CENTAVO, rounding=ROUND_HALF_UP
        )

    def detalhes(self) -> tuple[str, ...]:
        return (f"Quartos: {self._quartos}",)
