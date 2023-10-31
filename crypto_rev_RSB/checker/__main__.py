from time import time
from tqdm import tqdm
from pwn import connect
from randcrack import RandCrack
from random import Random as SystemRandom, SystemRandom as Random
from Crypto.Util.number import long_to_bytes, isPrime, getPrime, inverse

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
        if type(self.random) == RandCrack:
            p = int(bin(self.random.predict_getrandbits(nbits))[2:].zfill(nbits), 2)
        else:
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

io = connect("rsb.challs.srdnlen.it", 1339)
r = SystemRandom(int(time()))
ROUNDS = 1337
KEYS = [(r.randint(11, 19), r.randint(1, 200)) for _ in range(ROUNDS)]

nbits = 512
rc = RandCrack()
for _ in tqdm(range(39)):
    io.sendline(b'1')
    io.sendline(str(nbits).encode())
    io.recvuntil(b'wmwwnwwmnn = ')
    p = int(io.recvline(False).decode())
    io.recvuntil(b'mmmwmnnwmwnww = ')
    SBOX = eval(io.recvline(False).decode())

    p = list(bin(p)[2:].zfill(nbits))
    res = ["?"] * nbits
    for i, ind in enumerate(SBOX):
        res[ind] = p[i]
    assert "?" not in res
    p = int("".join(res), 2)

    l, r = p >> (nbits//2), p % 2**(nbits//2)
    for k in reversed(range(ROUNDS)):
        l, r = r ^ RSA()._f(l, k, nbits), l

    p = l << (nbits//2) | r

    tmp = bin(p)[2:].zfill(nbits)
    chunks = [tmp[i:i+32] for i in range(0, len(tmp), 32)]

    for chunk in chunks[::-1]:
        rc.submit(int(chunk, 2))

rsa = RSA()
rsa.random = rc

io.sendline(b'4')

io.recvuntil(b'nwnnnwwwwmnmmmn = ')
SBOX = eval(io.recvline(False).decode())

io.recvuntil(b'mnnmwnnnnmmw = ')
c = int(io.recvline(False).decode())
io.recvuntil(b'nwnnnwwwwmnmmmn = ')
e = int(io.recvline(False).decode())
io.recvuntil(b'wnnwmmmwmmwmm = ')
n = int(io.recvline(False).decode())

p, _, _ = rsa.genPrimes(1024, SBOX)
p = rsa.nextPrime(p)

assert n % p == 0

q = n // p

phi = (p-1)*(q-1)
d = inverse(e, phi)

flag = long_to_bytes(rsa.decrypt(c, d, n)).decode()

print(flag)

io.close()
