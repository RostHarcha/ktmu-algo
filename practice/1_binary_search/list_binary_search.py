def binary_search(arr: list[int], target: int) -> int:
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (right + left) // 2
        value = arr[mid]
        if target < value:
            right = mid - 1
        elif target > value:
            left = mid + 1
        else:
            return mid
    return -1


def is_sorted(arr: list[int]) -> bool:
    for i in range(len(arr) - 2):
        if arr[i] > arr[i + 1]:
            return False
    return True


def main() -> None:
    arr = list(
        map(
            int,
            input("enter sorted array using ` ` as delimeter: ").split(" "),
        )
    )
    if not is_sorted(arr):
        print("array must be sorted")
        return
    target = int(input("enter target: "))
    n = binary_search(arr, target)
    if n == -1:
        print("target not found")
        return
    print(f"target found on pos {n}")


if __name__ == "__main__":
    main()
