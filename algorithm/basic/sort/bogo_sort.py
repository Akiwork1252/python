import random
from typing import List

count = 0


def in_order(numbers: List[int]) -> bool:
    return all([numbers[i] <= numbers[i+1] for i in range(len(numbers)-1)])
    # for i in range(len(numbers)-1):
    #     if numbers[i] > numbers[i+1]:
    #         return False
    # return True


def bogo_sort(numbers: List[int]) -> List:
    global count
    while not in_order(numbers):
        random.shuffle(numbers)
        count += 1
    return numbers


if __name__ == '__main__':
    num_list = [random.randint(1, 10) for _ in range(5)]
    print(num_list)
    print((bogo_sort(num_list)))
    print('count:', count)
