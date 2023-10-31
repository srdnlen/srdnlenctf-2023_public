all: compile strip xor

compile:
	@echo compiling...
	@avr-gcc -O3 -static -DF_CPU=16000000UL -mmcu=atmega328p -o main.elf complex_chall.c

strip:
	@echo stripping...
	@avr-strip main.elf

xor:
	@python3 xor.py -i main.elf -o main.enc -p 69
