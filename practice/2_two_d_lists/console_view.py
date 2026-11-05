from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from hall import Hall


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
                ret += f"\n{seat.row + 1}"
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
                price = self.hall.get_price(seat.row)
                total_revenue += price
                stats[seat.row].revenue += price
            else:
                stats[seat.row].free += 1
        ret = "Статистика по рядам:\n"
        for row, row_data in stats.items():
            ret += f"Ряд {row + 1}: свободно {row_data.free}, выручка {row_data.revenue}\n"
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
            ret += f"Место {col + 1}: занято {reserved}\n"
            if reserved == most_popular_value:
                most_popular.add(col)
            elif reserved >= most_popular_value:
                most_popular = {col}
                most_popular_value = reserved
        most_popular_str = ", ".join(str(i + 1) for i in most_popular)
        ret += f"Самые популярные места: {most_popular_str} ({most_popular_value} занято)"
        return ret
