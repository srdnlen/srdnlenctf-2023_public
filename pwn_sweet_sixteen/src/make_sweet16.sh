#!/bin/bash

export PATH=$PATH:/home/kali/Downloads/elks-master/elks/tools/bin:/home/kali/Downloads/elks-master/cross/bin/
../cross/bin/ia16-elf-gcc -masm=intel -static -s -maout-symtab -v -melks-libc -mcmodel=small -o ./sweet16 sweet16.c
