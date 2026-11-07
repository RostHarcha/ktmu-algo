from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from hall import Hall, SeatNotExistsError, SeatReservedError


class ConsoleHallView:
    def __init__(self, hall: Hall) -> None:
        self.hall = hall

    def get_seating_plan(self) -> str:
        ret = "Схема зала:\n"
        seats_hint = "\t".join(
            str(i) for i in range(1, self.hall.max_seats + 1)
        )
        ret += f"\t{seats_hint}"
        last_row = -1
        for seat in self.hall:
            if seat.row > last_row:
                last_row = seat.row
                ret += f"\n{seat.row}"
            reserved = "X" if seat.reserved else "."
            ret += f"\t{reserved}"
        return ret

    def get_rows_stats(self) -> str:
        @dataclass
        class RowStats:
            free: int = 0
            revenue: Decimal = Decimal(0)

        total_reserved = 0
        total_revenue = Decimal(0)
        stats = defaultdict[int, RowStats](RowStats)
        for seat in self.hall:
            if seat.reserved:
                total_reserved += 1
                total_revenue += seat.price
                stats[seat.row].revenue += seat.price
            else:
                stats[seat.row].free += 1
        ret = "Статистика по рядам:\n"
        for row, row_data in stats.items():
            ret += f"Ряд {row}: свободно {row_data.free}, выручка {row_data.revenue}\n"
        ret += f"Общая выручка: {total_revenue}\n"
        occupancy = (
            Decimal(total_reserved)
            / Decimal(self.hall.total_seats)
            * Decimal(100)
        ).quantize(Decimal("100.00"))
        ret += f"Заполненность зала: {occupancy}% ({total_reserved}/{self.hall.total_seats})"
        return ret

    def get_columns_stats(self) -> str:
        stats = defaultdict[int, int](int)
        for seat in self.hall:
            stats[seat.col] += int(seat.reserved)
        most_popular = set[int]()
        most_popular_value = 0
        ret = "Статистика по местам:\n"
        for col, reserved in stats.items():
            ret += f"Место {col}: занято {reserved}\n"
            if reserved == most_popular_value:
                most_popular.add(col)
            elif reserved >= most_popular_value:
                most_popular = {col}
                most_popular_value = reserved
        most_popular_str = ", ".join(map(str, most_popular))
        ret += f"Самые популярные места: {most_popular_str} ({most_popular_value} занято)"
        return ret

    def get_reserve(self, orders: list[list[int]]) -> str:
        ret = "Бронирование:"
        for row, seat in orders:
            ret += f"\nБронирование ряд {row} место {seat}:\t"
            try:
                self.hall.set_reserved(row, seat, True)
            except SeatNotExistsError:
                ret += "Ошибка: место не существует"
            except SeatReservedError:
                ret += "Ошибка: место занято"
            else:
                ret += "Успешно"
        return ret

    def get_multi_order(self, k: int) -> str:
        ret = "Места для компании:"
        for row, (from_seat, to_seat) in self.hall.multi_order(k).items():
            ret += f"\nРяд {row}\tместа {from_seat}-{to_seat}"
        return ret

    def get_lonely_seats(self) -> str:
        ret = "Одинокие места:"
        for seat in self.hall.lonely_seats():
            ret += f"\nРяд {seat.row} место {seat.col}"
        return ret

    def get_best(self) -> str:
        best = self.hall.find_best()
        best_str = f"Ряд {best.row} место {best.col}" if best else "Не найдено"
        return f"Лучшее место: {best_str}"
