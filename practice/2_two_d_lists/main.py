from console_view import ConsoleHallView
from hall import Hall, HallRowConfig

hall_list: list[list[int]] = [
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
]

prices_list: list[int] = [
    250,
    250,
    350,
    400,
    400,
    350,
    300,
    300,
]  # цена места в каждом ряду, руб.


def main() -> None:
    hall = Hall(
        config=[
            HallRowConfig(
                price=price,
                seats=len(row),
                initial=list(map(bool, row)),
            )
            for row, price in zip(hall_list, prices_list, strict=True)
        ]
    )
    hall_view = ConsoleHallView(hall)
    print(hall_view.get_seating_plan())
    print("===")
    print(hall_view.get_rows_stats())
    print("===")
    print(hall_view.get_columns_stats())


if __name__ == "__main__":
    main()
