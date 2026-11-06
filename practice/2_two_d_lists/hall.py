from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal


class SeatNotExistsError(Exception):
    pass


class SeatReservedError(Exception):
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
    price: Decimal


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
        """Нумерация с 1"""
        if row < 1 or seat < 1:
            raise SeatNotExistsError
        value = bool(value)
        if value and self.get_reserved(row, seat):
            raise SeatReservedError
        try:
            self.rows[row - 1][seat - 1] = value
        except IndexError as exc:
            raise SeatNotExistsError from exc

    def get_reserved(self, row: int, seat: int) -> bool:
        """Нумерация с 1"""
        if row < 1 or seat < 1:
            raise SeatNotExistsError
        try:
            return self.rows[row - 1][seat - 1]
        except IndexError as exc:
            raise SeatNotExistsError from exc

    def get_price(self, row: int) -> Decimal:
        """Нумерация с 1"""
        if row < 1:
            raise SeatNotExistsError
        try:
            return self.prices[row - 1]
        except IndexError as exc:
            raise SeatNotExistsError from exc

    def _get_seat(self, row: int, col: int) -> Seat:
        return Seat(
            row=row + 1,
            col=col + 1,
            reserved=self.rows[row][col],
            price=self.get_price(row + 1),
        )

    def __iter__(self) -> Iterator[Seat]:
        for row, row_data in enumerate(self.rows):
            for col in range(len(row_data)):
                yield self._get_seat(row, col)

    def multi_order(self, k: int) -> dict[int, tuple[int, int]]:
        ret: dict[int, tuple[int, int]] = {}
        for row_i, row in enumerate(self.rows):
            l = 0
            r = -1
            while r + 1 < len(row):
                r += 1
                if row[r]:
                    l = r + 1
                elif r - l + 1 == k:
                    ret[row_i + 1] = (l + 1, r + 1)
                    break
        return ret

    def lonely_seats(self) -> Iterator[Seat]:
        for row, row_data in enumerate(self.rows):
            col = 0
            for col in range(len(row_data)):
                if row_data[col]:
                    continue
                left_lonely = col == 0 or row_data[col - 1]
                right_lonley = col == len(row_data) - 1 or row_data[col + 1]
                if left_lonely and right_lonley:
                    yield self._get_seat(row, col)
