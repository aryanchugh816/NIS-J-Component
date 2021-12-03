
# Function to check if a number is prime or not
def is_prime(a):
    if a > 1:
        for i in range(2, a):
            if (a % i) == 0:
                return (0)
            else:
                return (1)
    else:
        return (0)

# Function to find the gcd of two integers using Euclidean algorithm
def gcd(p, q):
    if q == 0:
        return p
    return gcd(q, p % q)

# Function to find the lcm of two integers
def lcm(p, q):
    return p * q // gcd(p, q)

# Function implementing extended euclidean algorithm
def egcd(e, phi):
    if e == 0:
        return (phi, 0, 1)
    else:
        g, y, x = egcd(phi % e, e)
    return (g, x - (phi // e) * y, y)

# Function to compute the modular inverse 
def modinv(e, phi):
    g, x, y = egcd(e, phi) 
    return x % phi

#Function to decrypt using RSA-CRT
def chineseremaindertheorem(dq, dp, p, q, c): 

    # Message part 1
    m1 = pow(c, dp, p) 

    # Message part 2 
    m2 = pow(c, dq, q) 
    qinv = modinv(q, p)
    h = (qinv * (m1 - m2)) % p 
    m = m2 + h * q
    return m

#Function to decrypt using just RSA 
def rsa(d,p,q,c):
    m3 = pow(c,d,(p*q)) 
    return m3
