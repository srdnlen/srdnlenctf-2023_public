import gdb
import string


def fill(flag):
    for j in range(len(flag)):
        gdb.execute("set $r" + str(j) + " = "  + flag[j], True, True)
    
    for i in range(len(flag), 28):
        gdb.execute("set $r" + str(i) + " = "  + "0x61", True, True)


def firsts_two(char):
    firsts = ""
    for i in char:
        for j in char:
            gdb.execute("set $r0 = " + i)
            gdb.execute("set $r1 = " + j) 
            gdb.execute("c")
            

            #checking if r24 equals 1 and r25, r26, r27 are equal to 0
            #we need r24 to be 1 because it will be add to r2 
            res = check()

            if res == 4:
                print(i, j)
                firsts += i + j
                return firsts
                #checking if r24 equals 1 and r25, r26, r27 are equal to 0
            else:
                gdb.execute("monitor r")
                res = 0
                #res != 4 means that our input in not correct and we have to restart the binary
                fill("")
    

def full_flag(firsts, char):
    flag = ""
    flag += firsts
    for j in 25:
        for i in char:
            fill(flag)
            gdb.execute("c")
            res = check()
            if res == 4:
                flag += i
                break
            else:
                gdb.execute("monitor r")
                res = 0
                
    return flag
        
def check():
    for i in range(5):
        gdb.execute("ni")
        # stop before ret
    
    reg = gdb.execute("p/x $r24")
    if "0x1" in reg:
            res += 1     
    for itr in range(25, 28):
        reg = gdb.execute("p/x $r" + str(itr))
        if "0x0" in reg:
            res += 1
    return res 


def main():
    
    firsts = ""
    flag = ""
    char = string.ascii_lowercase + string.digits + "_"

    gdb.execute("br *0xcd8") # break before load instruction
    gdb.execute("br *0xd5c") # break before ijmp   
    
    fill()
    #filling our buffer with "a"
    
    firsts = ""
    firsts = firsts_two(char)
    #bruteforcing the firsts two characters of our buffer
    
    flag = full_flag(firsts, char)
    #we can keep bruteforcing one byte at a time to find the full flag
    print(flag)
                
               
if __name__ == "__main__":
    main()
