import random
from typing import List, NewType


IndexNum = NewType('IndexNum', int)


def binary_search(numbers: List[int], value: int) -> int:
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == value:
            return mid
        elif numbers[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_search2(numbers: List[int], value: int) -> IndexNum:
    def _binary_search(numbers: List[int], value: int,
                      left: IndexNum, right: IndexNum) -> IndexNum:

        if left > right:
            return -1

        mid = (left + right) // 2
        if numbers[mid] == value:
            return mid
        elif numbers[mid < value]:
            return _binary_search(numbers, value, mid + 1, right)
        else:
            return _binary_search(numbers, value, 0, len(numbers)-1)

    return _binary_search(numbers, value, 0, len(numbers)-1)


if __name__ == '__main__':
    num_list = [random.randint(1, 10) for _ in range(10)]
    print(num_list)
    print(binary_search(num_list, 7))
    print(binary_search2(num_list, 7))
    
