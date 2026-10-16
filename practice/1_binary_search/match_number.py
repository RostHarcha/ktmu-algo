import math


def binary_search(left: int, right: int) -> int:
    step = 1
    while left <= right:
        mid = (right + left) // 2
        print(f"{step=}, {left=}, {right=}, {mid=}")
        comp = input(f"is your target <, > or = to {mid}: ")
        if comp == "<":
            print(f"target < {mid} -> target to the left")
            right = mid - 1
        elif comp == ">":
            print(f"target > {mid} -> target to the right")
            left = mid + 1
        elif comp == "=":
            print(f"target == {mid} -> found!")
            return step
        else:
            print("enter `<`, `>` or `=`")
            continue
        step += 1
    return -1


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt)
        try:
            return int(value)
        except:  # noqa: E722
            print("value must be int.")


def main() -> None:
    min_value = input_int("enter min value: ")
    max_value = input_int("enter max value: ")
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    steps = binary_search(min_value, max_value)
    if steps == -1:
        print(f"target not in range [{min_value}, {max_value}]")
    else:
        print(f"target found in {steps} steps.")
    total = max_value - min_value + 1
    max_steps = math.ceil(math.log2(total + 1))
    print(
        f"theoretical max number of steps to find number in range {total} is {max_steps}"
    )


if __name__ == "__main__":
    main()
