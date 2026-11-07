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

orders: list[list[int]] = [
    [3, 7],
    [1, 1],
    [8, 5],
    [10, 2],
    [4, 0],
]

def new_hall():
    hall1 = [[0 for col in range(6)] for row in range(5)]
    hall1[2][3] = 1
    # [[0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 1, 0, 0],
    #  [0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0]]

    print(f"Зал 1: {hall1}")
    hall2 = [[0] * 6] * 5
    hall2[2][3] = 1
    # [[0, 0, 0, 1, 0, 0],
    #  [0, 0, 0, 1, 0, 0],
    #  [0, 0, 0, 1, 0, 0],
    #  [0, 0, 0, 1, 0, 0],
    #  [0, 0, 0, 1, 0, 0]]
    print(f"Зал 2: {hall2}")
    # Результаты различаются, потому что hall2 создаеся с помощью ссылок:
    # [[0] * 6] - создается список (неизменяемый объект в памяти - ссылка на него)
    # при умножении его - копируется ссылка


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
    print("===")
    print(hall_view.get_reserve(orders))
    print("===")
    print(hall_view.get_multi_order(4))
    print("===")
    print(hall_view.get_lonely_seats())
    print("===")
    new_hall()
    print("===")
    print(hall_view.get_seating_plan())
    print("===")
    print(hall_view.get_best())


if __name__ == "__main__":
    main()
