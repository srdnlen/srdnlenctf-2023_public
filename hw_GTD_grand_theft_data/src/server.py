#!/usr/bin/python3

import time
import string
import random

data_watcher = False
cache = 0
main_enc = None
internal_constants_name = [
    'MODELNO',
    'CONSTVER',
    'PRODUCT',
    'COUNTRY',
    'CONSIZE',
    'MAXCONST',
    'PRODID',
    'CKSENA',
    'PREFLAG',
    'FLAG',
    'NOTDEF',
    'NOTDEF'
]

internal_memory_values = [
    1, # MODELNO
    1, # CONSTVER
    '74x6969', # PRODUCT
    'Italy', # COUNTRY
    '12K', # CONSIZE
    12, # MAXCONST
    'RIFHSBQW', # PRODID
    0, # CKSENA
    'srdnlen', # PREFLAG
    'srdnlen{THIS_IS_FAKE}', # FLAG
    0, # NOTDEF
    0 # NOTDEF
] + [0] * 20

def print_output(avb, status, data_out):
    print(f'avb|status|data_out[8] => {avb}{status}{data_out}')

def validate_input(op):
    if len(op) > 32:
        op = op[:32]
    elif len(op) < 32:
        op = '0' * (32 - len(op)) + op

    return None if not all(c in '01' for c in op) else op

def interpreter(op):
    global data_watcher
    global main_enc
    global internal_constants_name
    global cache
    global internal_memory_values

    opcode = int(op[:4], 2)
    reg_addr = int(op[4:12], 2)
    reg_val = int(op[12:32], 2)
    if opcode == 0b1100: # legge dalla rom esterna (manda il programma)
        if reg_val >= 8*1024:
            print_output(0, 1, bin(0)[2:].zfill(8))
        elif reg_val >= len(main_enc) and reg_val < 8*1024:
            print_output(1, 0, bin(0)[2:].zfill(8))
        else:
            print_output(1, 0, bin(main_enc[reg_val])[2:].zfill(8))
    elif opcode == 0b0001:
        for c in internal_constants_name:
            for b in c.encode('ascii'):
                print_output(1, 0, bin(b)[2:].zfill(8))
                print_output(0, 0, bin(b)[2:].zfill(8))
    elif opcode == 0b0010: # empty value
        if reg_addr > len(internal_memory_values):
            print_output(0, 1, bin(0)[2:].zfill(8))
        else:
            internal_memory_values[reg_addr] = 0
    elif opcode == 0b0011: # esegui il flush della cache
        print_output(0, 0, bin(cache)[2:].zfill(8))
    elif opcode == 0b0100: # abilita il pin di status, OK
        print_output(1, 1, bin(0)[2:].zfill(8))
    elif opcode == 0b0101: # disabilita il pin di status, OK
        print_output(1, 1, bin(0)[2:].zfill(8))
    elif opcode == 0b0110: # integrity check (disabilitato), OK
        print_output(0, 1, bin(0)[2:].zfill(8))
    elif opcode == 0b0111: # imposta il valore nella rom
        pass
    elif opcode == 0b1000: # ottieni il valore nella rom
        pass
    elif opcode == 0b1001: # copy value
        pass
    elif opcode == 0b1010: # is empty
        pass
    elif opcode == 0b1011: # enable data watcher, OK
        data_watcher = True
    elif opcode == 0b1101: # disable data watcher, OK
        data_watcher = False
    elif opcode == 0b1110: # get data watcher
        pass

def main():
    global main_enc
    with open('main.enc', 'rb') as f:
        main_enc = f.read()
    #print(len(main_enc))
    while True:
        try:
            op = validate_input(input("op[32] <= "))
            if op is None:
                print('Invalid input')
                continue

            interpreter(op)
        except KeyboardInterrupt:
            #pass
            exit(0)

if __name__ == '__main__':
    print('Welcome to the USB2Parallel CLI!')
    print('Checking drivers', end='')
    for _ in range(3):
        print('.', end='')
        time.sleep(1)
    print('done')
    time.sleep(2)
    print('Checking devices', end='')
    for _ in range(1):
        print('.', end='')
        time.sleep(0.5)
    try:
        id = ''.join([string.ascii_uppercase[random.randint(0, len(string.ascii_uppercase))] for _ in range(8)])
        print(f"found 1 device with serialID: {id}")
        internal_memory_values[6] = id
    except:
        print(f"found 1 device with serialID: RIFHSBQW")
    print(f'Device info:\n\tChip 74x6969\n\tManufacter: srdnlen\n\tInput alias: OP (32bit wide)\n\tOutput alias: AVB|STATUS|DATA_OUT (8bit wide)')
    main()
