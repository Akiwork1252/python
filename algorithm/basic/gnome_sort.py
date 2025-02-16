import random
from typing import List


def gnome_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    index = 0
    while index < len_numbers:
        if index == 0:
            index += 1
        if numbers[index] >= numbers[index-1]:
            index += 1
        else:
            numbers[index], numbers[index-1] = numbers[index-1], numbers[index]
            index -= 1

    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(gnome_sort(num_list))
