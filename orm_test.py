
#loop.close()
'''def _odd_iter():
    n = 1
    while n<9:
        n = n + 2
        yield n
def _not_divisible(n):
    def m(x):
        return x % n > 0
    return m    
def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(lambda x: x % n > 0, it)  # 构造新序列
        
for n in primes():
    if n < 1000:
        print(n)
    else:
        break 
l = [x for x in range(10)]
 
j = [x for x in range(10)]
 
 
 
def func(n):
    def m(x):
        return x % n > 0
    return m   
    #return lambda x: x != i#筛选出与i不相同的数
 
for i in range(1,10):
 
    j = filter(func(i), j)#不同处
 
for i in range(1,10):
 
    l = filter(lambda x: x % i > 0, l)  #不同处 
print(list(l))
 
print(list(j))
'''
def count():
    funcs=[]
    n = 0
    while n < 10:
        n += 1
        def f(i):
            return i == n
        funcs.append(f)
    return funcs
lam = [x for x in range(10)]
 
j = [x for x in range(10)]
def func(n):
    def m(x):
        return x==n
    return m   
    #return lambda x: x != i#筛选出与i不相同的数
 
for i in range(10):
 
    j = filter(func(i), j)  #不同处 
for i in range(10):
 
    lam = filter(lambda x: x==i, lam)  #不同处 
print(list(j))
print(list(lam))
def E(x, n):
    print('x:', x, 'n:', n)
    
def Md():
    func=[]
    for i in range(10):
        def m():
            print(i)
        func.append(m)
    return func    
for m in Md():
    m()

