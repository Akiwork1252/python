import random
from typing import List


def comb_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    gap = len_numbers
    swapped = True
    while gap != 1 or swapped:
        gap = int(gap/1.3)
        if gap < 1:
            gap = 1
        swapped = False

        for i in range(0, len_numbers-gap):
            if numbers[i] > numbers[i+gap]:
                numbers[i], numbers[i+gap] = numbers[i+gap], numbers[i]
                swapped = True

    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(comb_sort(num_list))
