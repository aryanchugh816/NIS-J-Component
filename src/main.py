import timeit
from utils import *
import sys
from generate_prime import return_prime
import random
import json

sys.setrecursionlimit(3000)

# Driver Code
# p = int(input("Enter the value for p: "))
# q = int(input("Enter the value for q: "))
# e = int(input("Enter the value for e: "))
# c = int(input("Enter the ctypt text: "))

# n = 4096


def start_comparison(n):

    print("Generating value for p")
    p = return_prime(n)
    print("Generating value for q")
    q = return_prime(n)

    m = random.getrandbits(10000)

    phi = (p-1)*(q-1)

    for i in range(65537, 2, -1):
        if(gcd(i, phi) == 1):
            e = i
            break

    print("Value of e: ", e)

    c = pow(m, e, p*q)

    print("Running Code")

    if(is_prime(p) == 0):
        print("Invalid input")
        exit(0)

    if(is_prime(q) == 0):
        print("Invalid input")
        exit(0)

    if(e >= (p*q)):
        print("invalid input")
        exit(0)

    # Calling RSA
    d = int(modinv(e, lcm(p - 1, q - 1)))
    # start = timeit.default_timer()
    # val1 = rsa(d, p, q, c)
    # stop = timeit.default_timer()
    t1 = timeit.timeit(lambda: rsa(d, p, q, c), number=1)
    # print ("RSA: \n",val1)
    # print('Time: ', stop - start)
    print("Time: ", t1)

    # Calling RSA_CRT
    d = int(modinv(e, lcm(p - 1, q - 1)))
    dq = pow(d, 1, q - 1)
    dp = pow(d, 1, p - 1)
    # start = timeit.default_timer()
    # val2 = chineseremaindertheorem(dq, dp, p, q, c)
    # stop = timeit.default_timer()
    # print ("RSA-CRT: \n", val2)
    # print('Time: ', stop - start)
    t2 = timeit.timeit(lambda: chineseremaindertheorem(
        dq, dp, p, q, c), number=1)
    print("Time: ", t2)

    values = {
        "p": p,
        "q": q,
        "e": e,
        "m": m,
        "c": c,
        "RSA Values": {
            "d": d
        },
        "RSA-CRT Values": {
            "d": d,
            "dp": dp,
            "dq": dq
        }
    }

    return (t1, t2, json.dumps(values))


# start_comparison(n=2048)
