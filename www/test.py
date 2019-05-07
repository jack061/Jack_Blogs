import functools
max2 = functools.partial(max, 10)
print(max2(3,4,5))
multipliers = [(lambda x, i=i:x * i) for i in range(0, 20)]
def adder(x):
    def wrapper(y):
        return x + y
    return wrapper

adder5 = adder(5)
# 输出 15
adder5(10)
# 输出 11
adder5(6)
L = [i * i for i in range( 5)]
for index,data in enumerate(L):
    print(index, ':', data)
