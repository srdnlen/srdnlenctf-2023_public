from pwn import *

host = '172.17.0.1'
port = 42069

conn = remote(host, port)
conn.recvuntil(b'op[32] <= ')

resp = []

try:
    for i in range(8 * 1024):
        print(f'Receiving byten {i}')
        conn.sendline(b'11' + bin(i)[2:].zfill(30).encode('ascii'))
        tmp = conn.recvuntil(b'op[32] <= ')
        tmp = tmp.split(b'=> ')[1].split(b'\n')[0]
        tmp = tmp[2:].decode('ascii')
        resp.append(int(tmp, 2))
except:
    pass

conn.close()

print(resp)

ba = bytes(resp)
with open('eepromdump.bin', 'wb') as file:
    file.write(ba)

print('Done! eepromdump.bin')