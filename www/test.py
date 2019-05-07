import functools
max2 = functools.partial(max, 10)
print(max2(3,4,5))