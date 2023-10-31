# srdnlenctf 2023

## my_first_game!

This challenge is an android game built in il2cpp but without anti-cheats (this is literally my first game, ofc I added the flag for the ctf, you can find it on google play store).

### Solution

To get all the money for the flag, you just have to use some program like Gameguardian or Cheat Engine.
My personal solution uses Bluestacks and Cheat-Engine for desktops. Very easily, you open the game on Bluestacks, you go to the first level and collect some coins (if you start looking for the value from 0 you can find too many possible variables and it can even crash Cheat Engine), then you open Cheat Engine and connect it to the HD-Player process, then search for value of your coins, then return to the game, get more coins, and search another time. This process is iterated until we have only two possible variables on Cheat Engine, at this point just modify these two variables with the price of the flag and that's it.