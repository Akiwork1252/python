import random
from typing import List


def shell_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    gap = len_numbers // 2
    while gap > 0:
        for i in range(gap, len_numbers):
            tmp = numbers[i]
            j = i
            while j >= gap and numbers[j-gap] > tmp:
                numbers[j] = numbers[j-gap]
                j -= gap
            numbers[j] = tmp
        gap //= 2
        
    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(shell_sort(num_list))
