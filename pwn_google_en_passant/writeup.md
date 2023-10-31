Google En Passant - Pwn

The core vulnerability is an out of bounds write during deserialization of the FEN notation of a chess position.

An error in the parsing logic means you can skip any amount of steps from 1 to 8, any number of times, before writing a piece.
This is because only closing the row with the specific "/" symbol resets the pointer position.
For instance, inputting the position `88888888888888888888888888888K//////// - 0` will place a "White king" byte 232 bytes off from the start of the board.

The second element in the game logic necessary to exploit the binary is the ability to create custom chess sets.
We will use this function to set the specific byte payloads corresponding to the bytes we want to write in our target offsets.
This isn't as simple as it sounds: a null byte will terminate your custom chess set prematurely. 
Our solve sorts the required bytes in reverse order, so that a null byte is always at the end of our input string.
(This does not avoid the situation in which a newline and a null byte were in the same pointer, but this did not happen in our tests).

By combining these two functionalities, we can craft a ROP chain beyond the main() return pointer and gain control of the system.
The input position has a hard limit of 100 characters, so it might be advisable to work one pointer (or even one byte if you're paranoid) at a time.
The main trick here is quite simple: the main() loop will not exit until we tell it to, 
and our ability to write arbitrarily instead of with a buffer overflow means all countermeasures are essentially useless.
We can take all the time we want and work one byte at a time. But please bear in mind the default timeout for the remote service is 30 seconds.

Once you've finished writing your ROP chain, all you have to do is exit normally. Depending on what your chain does, you can either open a shell on the system,
dump the process environment (you should see the flag here as well), or read the flag.txt file directly.

The file src/exploit.py implements an execve("/bin/sh") ROP chain one byte at a time.
