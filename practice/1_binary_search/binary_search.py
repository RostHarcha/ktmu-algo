import math


def binary_search(
    left: int,
    right: int,
    target: int,
    step: int = 1,
) -> int:
    if not (left <= target <= right):
        return -1
    mid = (right + left) // 2
    print(f"{step=}, {left=}, {right=}, {mid=}", end=" ")
    if target == mid:
        print(f"{target} == {mid} -> found!")
        return step
    if target < mid:
        print(f"{target} < {mid} -> target to the left")
        return binary_search(left, mid - 1, target, step + 1)
    print(f"{target} > {mid} -> target to the right")
    return binary_search(mid + 1, right, target, step + 1)


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt)
        try:
            return int(value)
        except:  # noqa: E722
            print("value must be int.")


def main() -> None:
    min = input_int("enter min value: ")
    max = input_int("enter max value: ")
    if min > max:
        print("error: min is greater than max")
        return

    target = input_int("enter target value: ")

    steps = binary_search(min, max, target)
    if steps == -1:
        print("error: target does not fall within [min, max]")
        return
    print(f"target {target} found in {steps} steps.")

    range = max - min
    max_steps = math.ceil(math.log2(range + 1))
    print(
        f"theoretical max number of steps to find number in range {range} is {max_steps}"
    )


if __name__ == "__main__":
    main()
