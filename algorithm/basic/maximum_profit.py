import random

# 2 <= n <= 200000
# 1 <= Rt <= 10**9

# データ
n = random.randint(2, 10)
num_list = [random.randint(1, 20) for _ in range(n)]
# 初期値
min_val = num_list[0]
max_diff = -float(10**9)


for i in range(1, n):
    max_diff = max(max_diff, num_list[i] - min_val)
    min_val = min(min_val, num_list[i])
print(f'List:{num_list}')
print(f'Max diff:{max_diff}')
