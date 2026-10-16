import math


def linear_search(left: int, right: int, target: int) -> int:
    l = left
    while l <= right:
        if l == target:
            return l - left + 1
        l += 1
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
    target = input_int("enter target value: ")
    if not (min_value <= target <= max_value):
        print("error: target does not fall within [min, max]")
        return
    steps = linear_search(min_value, max_value, target)
    print(f"target {target} found in {steps} steps.")
    total = max_value - min_value + 1
    max_steps = math.ceil(math.log2(total + 1))
    print(
        f"theoretical max number of steps to find number in range {total} is {max_steps}"
    )


if __name__ == "__main__":
    main()
