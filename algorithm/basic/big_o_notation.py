import random


# o(1)
def func0(numbers):
    return numbers[0]


# o(n)
def func1(numbers):
    for num in numbers:
        print(num)


# o(log(n))
def func2(n):
    if n < 1:
        return
    else:
        print(n)
        func2(n/2)


# o(n * log(n))
def func3(n):
    for i in range(int(n)):
        print(i, end='')
    if n <= 1:
        return
    print()
    func3(n/2)


# o(n**2)
def func4(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            print(numbers[i], numbers[j])
        print()


if __name__ == '__main__':
    num_list = [1, 2, 3, 4, 5]
    print('*'*5, 'o(1)', '*'*5)
    print(func0(num_list))
    print('*'*5, 'o(n)', '*'*5)
    func1(num_list)
    print('*'*5, 'o(log(n))', '*'*5)
    func2(10)
    print('*'*5, 'o(n*log(n))', '*'*5)
    func3(10)
    print('*'*5, 'o(n**2)', '*'*5)
    func4(num_list)


