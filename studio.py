"""Regra de calculo para estudios."""

from decimal import Decimal

from imovel import Imovel


class Studio(Imovel):
    """Estudio com pacote inicial de duas vagas ou sem estacionamento."""

    def __init__(self, vagas: int) -> None:
        if vagas != 0 and vagas < 2:
            raise ValueError("O estúdio permite 0 vagas ou pelo menos 2 vagas.")

        adicionais: list[tuple[str, Decimal]] = []
        if vagas >= 2:
            adicionais.append(("Pacote inicial (2 vagas)", Decimal("250.00")))
            for numero in range(3, vagas + 1):
                adicionais.append((f"Vaga adicional {numero - 1}", Decimal("60.00")))

        super().__init__("Estúdio", Decimal("1200.00"), tuple(adicionais))
        self._vagas = vagas

    @property
    def vagas(self) -> int:
        return self._vagas

    def detalhes(self) -> tuple[str, ...]:
        return (f"Vagas contratadas: {self._vagas}",)
