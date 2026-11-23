"""Regra de calculo para casas."""

from decimal import Decimal

from imovel import Imovel


class Casa(Imovel):
    """Casa de um ou dois quartos, com garagem opcional."""

    def __init__(self, quartos: int, possui_garagem: bool) -> None:
        if quartos not in (1, 2):
            raise ValueError("A casa deve ter 1 ou 2 quartos.")

        adicionais: list[tuple[str, Decimal]] = []
        if quartos == 2:
            adicionais.append(("Adicional de 2 quartos", Decimal("250.00")))
        if possui_garagem:
            adicionais.append(("Garagem", Decimal("300.00")))

        super().__init__("Casa", Decimal("900.00"), tuple(adicionais))
        self._quartos = quartos
        self._possui_garagem = possui_garagem

    @property
    def quartos(self) -> int:
        return self._quartos

    @property
    def possui_garagem(self) -> bool:
        return self._possui_garagem

    def detalhes(self) -> tuple[str, ...]:
        return (f"Quartos: {self._quartos}",)
