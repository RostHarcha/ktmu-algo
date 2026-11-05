from dataclasses import dataclass
from decimal import Decimal


class NonexistentSeatError(Exception):
    pass


@dataclass(frozen=True)
class HallRowConfig:
    price: Decimal | float | int
    seats: int
    initial: list[bool] | None = None


@dataclass(frozen=True)
class Seat:
    row: int
    col: int
    reserved: bool


class Hall:
    def __init__(self, config: list[HallRowConfig]) -> None:
        self.rows: list[list[bool]] = []
        self.prices: list[Decimal] = []
        self.max_seats: int = 0
        self.total_seats: int = 0
        for row in config:
            if row.seats > self.max_seats:  # noqa: PLR1730
                self.max_seats = row.seats
            initial = row.initial or [False for _ in range(row.seats)]
            if len(initial) != row.seats:
                raise RuntimeError(
                    "Seats count and initial len unmatch", initial, row.seats
                )
            self.total_seats += row.seats
            self.rows.append(initial)
            self.prices.append(Decimal(row.price))

    def set_reserved(self, row: int, seat: int, value: bool | int) -> None:
        try:
            self.rows[row][seat] = bool(value)
        except IndexError as exc:
            raise NonexistentSeatError from exc

    def get_reserved(self, row: int, seat: int) -> bool:
        try:
            return self.rows[row][seat]
        except IndexError as exc:
            raise NonexistentSeatError from exc

    def get_price(self, row: int) -> Decimal:
        try:
            return self.prices[row]
        except IndexError as exc:
            raise NonexistentSeatError from exc

    def __iter__(self):
        for row, row_data in enumerate(self.rows):
            for col, reserved in enumerate(row_data):
                yield Seat(row=row, col=col, reserved=reserved)
