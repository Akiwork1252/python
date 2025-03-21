import random
from typing import List


def merge_sort(data: list, l: int, m: int, r: int) -> list:
    len_left, len_right = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len_left):
        left.append((data[l + i]))
    for i in range(0, len_right):
        right.append(data[m + 1 + i])

    i, j, k = 0, 0, l
    while i < len_left and j < len_right:
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1

    while i < len_left:
        data[k] = left[i]
        i += 1
        k += 1

    while j < len_right:
        data[k] = right[j]
        j += 1
        k += 1

    return data


def insertion_sort(data: list, left: int, right: int) -> list:
    for i in range(left+1, right+1):
        tmp = data[i]
        j = i - 1
        while j >= left and data[j] > tmp:
            data[j + 1] = data[j]
            j -= 1

        data[j + 1] = tmp
    return data


def tim_sort(data: list, size: int = 32) -> list:
    n = len(data)
    for i in range(0, n, size):
        insertion_sort(data, i, min((i + 31), (n - 1)))

    while size < n:
        for left in range(0, n, 2 * size):
            mid = left + size - 1
            right = min((left + 2 * size - 1), (n - 1))
            merge_sort(data, left, mid, right)
        size = 2 * size
    return data


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(tim_sort(num_list))
