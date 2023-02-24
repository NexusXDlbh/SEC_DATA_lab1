import random

first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
    return(random.randrange(2**(n-1)+1, 2**n-1))

def getLowLevelPrime(n):
    while True:
        prime_generated = nBitRandom(n)

        for divisor in first_primes_list:
            if prime_generated % divisor == 0 and divisor**2 <= prime_generated:
                break
            else: return prime_generated

def isMiller_Rabin_Test(p):
    # 0.
    # if p < 3 or (p & 1 == 0):
    #     return p == 2

    # 1. preparation
    m = p-1 # p 奇 -> m 偶
    q = 0

    while m%2 == 0 :
        # print("1") tested √
        q += 1  
        m = m//2 # 右移做快速÷2 
    # while 循环结束时满足如下条件
    # p-1 = 2^q · m 
    
    assert(p-1 == 2**q * m)
    tested = [] # 存放测试过的数据
    
    # 2.算法开始 
    t = 20 # 20轮足够了
    for _ in range(t):
        composite = True
        # picking a random integer -> a
        a = random.randint(2,p-2)
        while a in tested:
            a = random.randint(2,p-2)
        tested.append(a)
        r = pow(a,m,p) # 快速模除
        if r == 1 or r == p-1:
            composite = False # 根据二次探测定理：如果满足if的条件，就是素数
        else:                 # 再次判断
            for j in range(1,q):
                r = (r * r)%p
                if r == p-1:
                    composite = False
                    break

        if composite:
            return False
    return True

def getGenerator(n):
    return( nBitRandom(n) )

def getLargePrime(n):
    while True:
        p = getLowLevelPrime(n)
        if not isMiller_Rabin_Test(p):
            continue
        else:
            print(n, "bit prime is: \n",p)
            break
    return p
