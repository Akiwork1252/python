import random
import time
from typing import List


def my_bubble_sort(numbers: List[int]) -> List[int]:
    n = len(numbers)
    while 2 <= n:
        for i in range(n-1):
            if numbers[i] > numbers[i+1]:
                num = numbers[i+1]
                numbers[i+1] = numbers[i]
                numbers[i] = num
        n -= 1
    return numbers


def bubble_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    for i in range(len_numbers):
        for j in range(len_numbers -1 - i):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers


def optimized_bubble_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    swapped = False  # 交換が発生したか記録
    for i in range(len_numbers):
        for j in range(len_numbers - 1 - i):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
                swapped = True
            # 交換されていなければループを抜ける
            if not swapped:
                break
    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 2000) for _ in range(10)]
    print(f'Before List: {num_list}')
    print(f'My Sorted List: {my_bubble_sort(num_list)}')
    print(f'Sorted List: {bubble_sort(num_list)}')
    print(f'GPT Sorted List: {optimized_bubble_sort(num_list)}')
