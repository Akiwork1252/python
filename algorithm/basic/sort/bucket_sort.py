import random
from typing import List


def insertion_sort(numbers: List[int]) -> List[int]:
    len_numbers = len(numbers)
    for i in range(1, len_numbers):
        tmp = 1
        j = i - 1

        while j >= 0 and numbers[j] > tmp:
            numbers[j+1] = numbers[j]
            j -= 1

        numbers[j+1] = tmp

    return numbers


def bucket_sort(numbers: List[int]) -> List[int]:
    max_num = max(numbers)
    len_numbers = len(numbers)
    size = max_num // len_numbers  # bucket sizeを適切に設定しないとエラーが発生する。修正の必要がある。
    print(max_num, len_numbers, size)

    buckets = [[] for _ in range(size)]
    print(buckets)
    for num in numbers:
        i = num // size
        if i != size:
            buckets[i].append(num)
        else:
            buckets[size-1].append(num)

    for i in range(size):
        insertion_sort(buckets[i])

    result = []
    for i in range(size):
        result += buckets[i]

    return result


if __name__ == '__main__':
    num_list = [random.randint(1, 100) for _ in range(10)]
    print(num_list)
    print(bucket_sort(num_list))
