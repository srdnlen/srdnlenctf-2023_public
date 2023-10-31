import os
import signal
from time import time
from random import Random as SystemRandom, SystemRandom as Random
from Crypto.Util.number import bytes_to_long, isPrime, getPrime

FLAG = os.getenv("FLAG", "srdnlen{REDACTED}").encode()
ROUNDS = 1337
r = SystemRandom(int(time()))
KEYS = [(r.randint(11, 19), r.randint(1, 200)) for _ in range(ROUNDS)]

class RSA:
    def __init__(self, seed=None):
        self.random = SystemRandom(seed)

    def _f(self, n, kn, nbits):
        o, m = KEYS[kn]
        return (n + o) * m % 2 ** (nbits//2)

    def nextPrime(self, n):
        n += 1
        while not isPrime(n):
            n += 1
        return n

    def genPrimes(self, nbits, SBOX=None):
        assert nbits % 2 == 0
        p = int(bin(self.random.getrandbits(nbits))[2:].zfill(nbits), 2)

        l, r = p >> (nbits//2), p % 2**(nbits//2)
        for k in range(ROUNDS):
            l, r = r, l ^ self._f(r, k, nbits)

        p = l << (nbits//2) | r

        if SBOX == None:
            rand = Random(int(time()))
            SBOX = rand.sample(population=range(nbits), k=nbits)

        p = list(bin(p)[2:].zfill(nbits))
        res = []
        for ind in SBOX:
            res += [p[ind]]
        p = int("".join(res), 2)

        return p, getPrime(nbits), SBOX

    def encrypt(self, m, e, n):
        return pow(m, e, n)

    def decrypt(self, c, d, n):
        return pow(c, d, n)

def menu():
    try:
        rsa = RSA(os.urandom(16))
        while True:
            choice = int(input(f"""
What do you want to do?
    1) Generate RSA primes
    2) Encrypt a message
    3) Decrypt a message
    4) Get the encrypted flag
    5) Exit

"""))
            match choice:
                case 1:
                    nbits = int(input("Number of bits: "))
                    assert nbits <= 1024
                    p, q, SBOX = rsa.genPrimes(nbits)
                    print(f"{p = }")
                    print(f"{q = }")
                    print(f"{SBOX = }")
                case 2:
                    m = bytes.fromhex(input("Message: "))
                    e = int(input("e: "))
                    n = int(input("n: "))
                    c = rsa.encrypt(bytes_to_long(m), e, n)
                    print(f"{c = }")
                case 3:
                    c = bytes.fromhex(input("Ciphertext: "))
                    d = int(input("d: "))
                    n = int(input("n: "))
                    m = rsa.decrypt(bytes_to_long(c), d, n)
                    print(f"{m = }")
                case 4:
                    p, q, SBOX = rsa.genPrimes(1024)
                    p = rsa.nextPrime(p)
                    print(f"{SBOX = }")
                    e = 65537
                    n = p*q
                    c = rsa.encrypt(bytes_to_long(FLAG), e, n)
                    print(f"{c = }")
                    print(f"{e = }")
                    print(f"{n = }")
                case 5:
                    exit(0)
                case _:
                    raise NotImplementedError
    except KeyboardInterrupt:
        raise
    except:
        raise Exception("Error")

if __name__ == "__main__":
    signal.alarm(300)
    print("Welcome to RSB, a super secure RSA service!")
    menu()
