from sage.all import *
from ecdsa import curves, util, SigningKey, VerifyingKey
from hashlib import sha224
from Crypto.Util.number import bytes_to_long
from pwn import process, remote
import os, ast

# https://eprint.iacr.org/2020/1506.pdf section 5.2.3

HOST = os.getenv("HOST", "babyornot.challs.srdnlen.it")
PORT = int(os.getenv("PORT", 1338))
io = remote(HOST, PORT)

vk = VerifyingKey.from_string(
    bytes.fromhex(io.recvline_contains(b"public key: ", keepends=False).decode().split(": ").pop()),
    curve=curves.NIST224p, hashfunc=sha224
)

signed_msgs = [ast.literal_eval(io.recvline(keepends=False).decode().split(": ").pop()) for _ in range(2)]
true_signs = [b"<From the mighty>", b"<For the players>"]

n = int(curves.NIST224p.order)
(m1, (r1, s1)), (m2, (r2, s2)) = signed_msgs
h1, h2 = [bytes_to_long(sha224(bytes.fromhex(m)).digest()) for m in [m1, m2]]
a1, a2 = [bytes_to_long(true_sign) * 2**44 for true_sign in true_signs]
l = 224 - 44

t = int(-pow(s1, -1, n) * s2 * r1 * pow(r2, -1, n) % n)
u = int((pow(s1, -1, n) * r1 * h2 * pow(r2, -1, n) - pow(s1, -1, n) * h1) % n)
u0 = int((a1 + t * a2 + u) % n)
K = 2**44

B = Matrix(ZZ, [
    [K, K * 2**l, K * t, K * t * 2**l, u0],
    [0, K * n, 0, 0, 0],
    [0, 0, K * n, 0, 0],
    [0, 0, 0, K * n, 0],
    [0, 0, 0, 0, n]
])

B = B.BKZ()

M, rhs = [], []
for row in B[:4]:
    M.append([x // K for x in map(int, row[:-1])])
    rhs.append(-int(row[-1]))

b1, c1, b2, c2 = map(int, Matrix(ZZ, M).solve_right(vector(ZZ, rhs)))
assert (b1 + 2**l * c1 + t * b2 + 2**l * t * c2 + u0) % n == 0

k1, k2 = a1 + b1 + 2**l * c1, a2 + b2 + 2**l * c2
d = int(pow(r1, -1, n) * (k1 * s1 - h1) % n)
assert d * vk.pubkey.generator == vk.pubkey.point

sk = SigningKey.from_secret_exponent(d, curve=curves.NIST224p, hashfunc=sha224)
assert vk.verify(sk.sign(b"OK"), b"OK")

msg = b"Could I have the flag?"
signed_msg = (msg.hex(), util.sigdecode_string(sk.sign(msg), n))
io.sendlineafter(b"Do you have a signed message for me? ", str(signed_msg).encode())
print(io.recvrepeat(1).decode())

io.close()
