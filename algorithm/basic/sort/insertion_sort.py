import random
from typing import List


def insertion_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    for i in range(1, len_numbers):
        tmp = numbers[i]
        j = i - 1
        while j >= 0 and numbers[j] > tmp:
            numbers[j+1] = numbers[j]
            j -= 1

        numbers[j+1] = tmp

    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(insertion_sort(num_list))
