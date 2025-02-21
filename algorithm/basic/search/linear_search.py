import random
from typing import List, NewType


IndexNum = NewType('IndexNum', int)


def linear_search(numbers: List[int], value: int) -> int:
    for i in range(0, len(numbers)):
        if numbers[i] == value:
            return i
    return -1


if __name__ == '__main__':
    num_list = [random.randint(1, 10) for _ in range(10)]
    print(num_list)
    print(linear_search(num_list, 7))

